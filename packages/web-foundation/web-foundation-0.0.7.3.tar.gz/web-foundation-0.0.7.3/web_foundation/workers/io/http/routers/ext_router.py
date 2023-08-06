from dataclasses import dataclass
from typing import List, Type, Callable

from pydantic import BaseModel
from sanic import Sanic
from sanic.router import Router

from web_foundation.workers.io.http.chaining import HandlerType, Protector


@dataclass
class RouteMethodConf:
    method_name: str
    protector: Protector | None
    in_dto: Type[BaseModel] | None
    out_dto: Type[BaseModel] | None
    handler: HandlerType
    response_fabric: Callable | None
    # chain: HandlerType
    version_prefix: str | None
    version: str | None


@dataclass
class RouteConf:
    app_name: str
    path: str
    methods: List[RouteMethodConf]


class ExtRouter(Router):
    chaining: Callable
    chains: List[RouteConf]

    def apply_routes(self, app: Sanic, *args, **kwargs):
        raise NotImplementedError
