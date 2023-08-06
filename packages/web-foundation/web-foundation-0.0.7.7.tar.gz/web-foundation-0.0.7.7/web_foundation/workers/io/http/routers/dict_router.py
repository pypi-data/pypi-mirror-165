import inspect
import re
from copy import deepcopy
from typing import Dict, Callable, Type

import loguru
from pydantic import BaseModel as PdModel

import sanic_ext
from sanic import Sanic
from sanic_ext.extensions.openapi.builders import SpecificationBuilder, OperationStore

from web_foundation.app.infrastructure.mdw_manager import ApiMiddlewareManager
from web_foundation.workers.io.http.routers.ext_router import ExtRouter, RouteMethodConf, RouteConf


def get_definition_with_correct_name(definitions: Dict) -> Dict:
    _definitions = {}
    for defin, _schema in definitions.copy().items():
        if "." in defin:
            _definitions[defin.split(".")[-2]] = _schema
        else:
            _definitions[defin] = _schema
    return _definitions


def get_model_schema(model: Type[PdModel]):
    """ Create schema from pydantic model and add all references to OpenAPI schemas """
    schema = model.schema(ref_template="#/components/schemas/{model}")
    components = {}
    if "definitions" in schema:
        definitions = get_definition_with_correct_name(schema.pop("definitions"))
        components.update(definitions)
    components.update({model.__name__: schema})
    spec = SpecificationBuilder()
    for component_name, component in components.items():
        spec._components["schemas"].update({component_name: component})
    return schema


def add_openapi_spec(uri: str, method_name: str, func: Callable, handler: Callable,
                     in_dto: Type[PdModel], out_dto: Type[PdModel]):
    # --- copy existed openapi params ---#
    if OperationStore().get(func):
        OperationStore()[handler] = deepcopy(OperationStore().get(func))
    # --- add query args ---#
    func_text = inspect.getsource(func)
    func_query_args = set(re.findall(r"request.args.get\(\"(\w*)\"\)", func_text))
    if func_query_args:
        for func_arg in func_query_args:
            handler = sanic_ext.openapi.parameter(func_arg)(handler)
    # --- add request body ---#
    if in_dto:
        if issubclass(in_dto, PdModel):
            schema = get_model_schema(in_dto)
            if not hasattr(OperationStore()[handler], "requestBody"):
                OperationStore()[handler].requestBody = {"content": {
                    "application/json": {'schema': schema},
                    "multipart/form-data": {'schema': schema}
                }}
            elif not OperationStore()[handler].requestBody.get("content"):
                OperationStore()[handler].requestBody['content'] = {
                    "application/json": {'schema': schema},
                    "multipart/form-data": {'schema': schema}
                }
            if not OperationStore()[handler].requestBody['content'].get("application/json"):
                OperationStore()[handler].requestBody['content'].update({"application/json": {'schema': schema}})
            elif not OperationStore()[handler].requestBody['content']["application/json"].get("schema"):
                OperationStore()[handler].requestBody['content']["application/json"].update({'schema': schema})
            else:
                for k, v in schema.items():
                    if isinstance(v, dict):
                        OperationStore()[handler].requestBody['content']["application/json"]['schema'][k].update(v)
                    else:
                        OperationStore()[handler].requestBody['content']["application/json"]['schema'][k] = v
            if not OperationStore()[handler].requestBody['content'].get("multipart/form-data"):
                OperationStore()[handler].requestBody['content'].update({"multipart/form-data": {'schema': schema}})
            elif not OperationStore()[handler].requestBody['content']["multipart/form-data"].get("schema"):
                OperationStore()[handler].requestBody['content']["multipart/form-data"].update({'schema': schema})
            else:
                for k, v in schema.items():
                    if isinstance(v, dict):
                        OperationStore()[handler].requestBody['content']["multipart/form-data"]['schema'][k].update(v)
                    else:
                        OperationStore()[handler].requestBody['content']["multipart/form-data"]['schema'][k] = v
    # --- add response ---#
    if out_dto:
        if issubclass(out_dto, PdModel):
            schema = get_model_schema(out_dto)
            existed_resp = OperationStore()[handler].responses.get("200")
            if not existed_resp:
                OperationStore()[handler].responses["200"] = {"content": {"application/json": {'schema': schema}},
                                                              "description": "OK"}
            else:
                if not existed_resp.get('content'):
                    existed_resp.update({"content": {"application/json": {'schema': schema}},
                                         "description": "OK"})
                elif not existed_resp['content'].get("application/json"):
                    existed_resp['content'].update({"application/json": {'schema': schema}})
                elif not existed_resp['content']["application/json"].get("schema"):
                    existed_resp['content']["application/json"].update({'schema': schema})
                else:
                    for k, v in schema.items():
                        if isinstance(v, dict):
                            existed_resp['content']["application/json"]['schema'][k].update(v)
                        else:
                            existed_resp['content']["application/json"]['schema'][k] = v
    # --- add tag ---#
    handler = sanic_ext.openapi.tag(uri.split("/")[1].capitalize())(handler)  # first path word

    # --- decription --- #
    # f = sanic_ext.openapi.description("hujkiikasdf;awerfl;jkasdfklj;asdfjkl;")(handler)
    # f = sanic_ext.openapi.summary("l;kasdjllww")(handler)

    # --- set operation id --- #
    handler = sanic_ext.openapi.operation(f"{method_name}~{uri}")(handler)
    return handler


class DictRouter(ExtRouter):
    _router_conf: Dict
    chaining: Callable
    mdw_manager: ApiMiddlewareManager | None
    versioning: bool

    def __init__(self, routes_config: Dict, chaining: Callable,
                 versioning: bool = True):
        super().__init__()
        self.chaining = chaining
        self._router_conf = routes_config
        self.chains = []
        self.versioning = versioning
        self._parse()

    def _parse(self):
        for app_route in self._router_conf.get("apps"):
            version_prefix = app_route.get("version_prefix")
            version_prefix = version_prefix if version_prefix else "/api/v"
            for endpoint, versions in app_route.get("endpoints").items():
                for version, params in versions.items():
                    methods_confs = []
                    endpoint_handler = params.pop("handler", None)
                    endpoint_protector = params.pop("protector", None)
                    endpoint_response_fabric = params.pop("response_fabric", None)
                    for method_name, method_params in params.items():
                        target_func = method_params.get('handler')
                        target_func = target_func if target_func else endpoint_handler
                        protector = method_params.get("protector")
                        protector = protector if protector else endpoint_protector
                        in_dto = method_params.get("in_dto")
                        out_dto = method_params.get("out_dto")
                        response_fabric = method_params.get("response_fabric")
                        response_fabric = response_fabric if response_fabric else endpoint_response_fabric

                        methods_confs.append(RouteMethodConf(method_name=method_name,
                                                             protector=protector,
                                                             in_dto=in_dto,
                                                             out_dto=out_dto,
                                                             handler=target_func,
                                                             response_fabric=response_fabric,
                                                             version_prefix=version_prefix,
                                                             version=version
                                                             ))

                    route = RouteConf(app_name=app_route.get("app_name"),
                                      path=endpoint,
                                      methods=methods_confs)
                    self.chains.append(route)

    def apply_routes(self, app: Sanic, mdw_manager: ApiMiddlewareManager = None, **kwargs):
        """
        If you want use chaining, please use partial(chain,validation_fnc=...,response_fabric=...)
        :param **kwargs:
        :param chaining:
        :return:
        """
        for route_conf in self.chains:
            for method_conf in route_conf.methods:
                if method_conf.response_fabric:
                    chain = self.chaining(
                        protector=method_conf.protector,
                        in_struct=method_conf.in_dto,
                        plugin_manager=mdw_manager,
                        response_fabric=method_conf.response_fabric)(method_conf.handler)
                else:
                    chain = self.chaining(
                        protector=method_conf.protector,
                        plugin_manager=mdw_manager,
                        in_struct=method_conf.in_dto)(method_conf.handler)

                chain = add_openapi_spec(uri=route_conf.path, method_name=method_conf.method_name,
                                         func=method_conf.handler,
                                         handler=chain, in_dto=method_conf.in_dto, out_dto=method_conf.out_dto)

                if self.versioning:
                    app.add_route(uri=route_conf.path, methods={method_conf.method_name.upper()},
                                  handler=chain,
                                  version_prefix=method_conf.version_prefix, version=method_conf.version)
                else:
                    app.add_route(uri=route_conf.path, methods={method_conf.method_name.upper()},
                                  handler=chain)

        # warn(f"Can't find dto or handler in imported module, suppressed exception: {e.__str__()}")
