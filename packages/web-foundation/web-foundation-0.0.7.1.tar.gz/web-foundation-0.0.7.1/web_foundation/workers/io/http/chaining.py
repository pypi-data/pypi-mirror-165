import os
from dataclasses import dataclass
from functools import wraps
from typing import Any, Callable, Type, Coroutine, TypeVar, Generic
from typing import Union, Dict, List

import loguru
from dependency_injector.wiring import Provide, inject
from pydantic import BaseModel as PdModel
from sanic import Request, json, HTTPResponse

from web_foundation.app.app import AppContainer
from web_foundation.app.infrastructure.mdw_manager import ApiMiddlewareManager
from web_foundation.utils.validation import validate_dto

DtoType = TypeVar("DtoType", bound=PdModel)


@dataclass
class ProtectIdentity:
    pass


ProtectIdentityType = TypeVar("ProtectIdentityType", bound=ProtectIdentity)


@dataclass
class InputContext(Generic[DtoType, ProtectIdentityType]):
    request: Request
    dto: DtoType | None
    identity: ProtectIdentity | None
    r_kwargs: Dict


Protector = Callable[[Request], Coroutine[Any, Any, ProtectIdentityType | None]]
DtoValidator = Callable[[Type[DtoType], Request], PdModel]
HandlerType = Callable[[InputContext, AppContainer], Coroutine[Any, Any, HTTPResponse]]

JSON = Union[Dict[str, Any], List[Any], int, str, float, bool, Type[None]]
TypeJSON = Union[Dict[str, 'JSON'], List['JSON'], int, str, float, bool, Type[None]]


async def protect(request: Request) -> ProtectIdentity | None:
    return None


def chain(protector: Protector = protect,
          in_struct: Type[PdModel] | None = None,
          plugin_manager: ApiMiddlewareManager = None,
          validation_fnc: DtoValidator = validate_dto,
          response_fabric: Callable[[TypeJSON], HTTPResponse] = json,
          ):
    def called_method(target: HandlerType):
        @wraps(target)
        @inject
        async def f(*args, container=Provide["<container>"], **kwargs):
            req: Request = args[0]
            prot_identity = await protector(req) if protector else None
            if in_struct:
                validated = validation_fnc(in_struct, req)
            else:
                validated = None
            incoming = InputContext(req, validated, prot_identity, kwargs)
            if plugin_manager:
                plugins = await plugin_manager.find_middleware_by_target(target.__name__)
                for plugin in await plugin_manager.find_middleware_by_target(target.__name__):
                    await plugin.exec_before(context=incoming, container=container)
                    # if plugin.override:
                    #     ret_val = await plugin.exec_override(context=incoming, container=container)
                    # else:
                    #     ret_val = await target(incoming, container)
                    # await plugin.exec_after(context=incoming, container=container, target_result=ret_val)
                if not plugins:
                    ret_val = await target(incoming, container)
                else:
                    overrides = [pl for pl in plugins if pl.override]
                    if overrides:
                        ret_val = await overrides[0].exec_override(context=incoming, container=container)
                    else:
                        ret_val = await target(incoming, container)
                    for plugin in plugins:
                        await plugin.exec_after(context=incoming, container=container, target_result=ret_val)
            else:
                ret_val = await target(incoming, container)
            return response_fabric(ret_val)

        return f

    return called_method
