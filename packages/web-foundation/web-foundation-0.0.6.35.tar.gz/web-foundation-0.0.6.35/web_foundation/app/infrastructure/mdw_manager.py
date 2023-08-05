from enum import Enum
from importlib.abc import FileLoader
from importlib.util import spec_from_loader
from typing import List, Type

from loguru import logger
from web_foundation.workers.io.http.mdw_obj import ApiMiddleware
from web_foundation.app.resources.cache.repo import AppStore
from web_foundation.app.resources.file_repo.repo import FileRepository, AppFileSections


class SourceCodeLoader(FileLoader):
    def __init__(self, fullname: str, source):
        super().__init__(fullname, source)
        self.path = source

    def get_source(self, fullname: str) -> str | bytes:
        return self.path


class ApiMiddlewareManager:
    debug: bool
    repo: FileRepository
    store: AppStore
    sections: Type[Enum]

    def __init__(self, repo: FileRepository, store: AppStore, debug: bool = False,
                 sections: Type[Enum] = AppFileSections):
        self.debug = debug
        self.repo = repo
        self.store = store
        self.sections = sections

    async def _import_middleware(self, pl: ApiMiddleware):
        middlewares = await self.store.get_item("middleware") if await self.store.get_item("middleware") else []
        try:
            spec = spec_from_loader(pl.name, loader=SourceCodeLoader(pl.name, pl.source))
            pl.import_it(spec)
            if pl not in middlewares:
                middlewares.append(pl)
            await self.store.set_item("middleware", middlewares)
        except Exception as e:
            if self.debug:
                logger.debug(f"Can't load plugin {pl.name}, cause {str(e)}")

    async def import_middleware(self):
        middlewares = await self.store.get_item("middleware") if await self.store.get_item("middleware") else []
        for pl in middlewares:
            await self._import_middleware(pl)

    async def configure_middleware(self, plugin: ApiMiddleware, *args, **kwargs) -> ApiMiddleware:
        """Set middleware name, target and enabled"""
        raise NotImplementedError

    async def _discover_middleware(self, filename) -> ApiMiddleware | None:
        async with (await self.repo.take(filename, self.sections.PLUGINS)) as file_:
            pl = ApiMiddleware(filename, await file_.read())
            pl = await self.configure_middleware(pl)
            if pl.name is None:
                raise AttributeError("ApiMiddleware name must be specified")
            middlewares = await self.store.get_item("middleware") if await self.store.get_item("middleware") else []
            if middlewares and pl in middlewares:
                middlewares.remove(pl)
            middlewares.append(pl)
            return pl

    async def discover_middleware(self):
        for filename in await self.repo.open_section(self.sections.PLUGINS):
            await self._discover_middleware(filename)

    async def add_new_middleware(self, filename: str):
        pl = await self._discover_middleware(filename)
        if pl:
            await self._import_middleware(pl)
            if self.debug:
                logger.debug(f"New plugin added {pl}")

    async def find_middleware_by_target(self, target: str) -> List[ApiMiddleware]:
        middlewares = await self.store.get_item("middleware")
        if not middlewares:
            return []
        else:
            cell_plugins: List[ApiMiddleware] = []
            for pl in middlewares:
                if pl.target == target and pl.enabled:
                    cell_plugins.append(pl)
            return cell_plugins

    #
    # async def reload_all_plugins(self):
    #     self.available_middlewares = []
    #     await self._drop_stored_plugins()
    #     await self.discover_middleware()
    #     await self.import_middleware()
    #     await self.store_middlewares()
