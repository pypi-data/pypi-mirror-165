from importlib.abc import FileLoader
from importlib.util import spec_from_loader
from typing import List

from loguru import logger

from web_foundation import settings
from web_foundation.app.events.store import StoreUpdateEvent
from web_foundation.app.resources.file_repo.repo import FileRepository, AppFileSections, GenFileSections
from web_foundation.app.resources.stores.store import AppStore
from web_foundation.workers.io.http.mdw_obj import ApiMiddleware


class SourceCodeLoader(FileLoader):
    def __init__(self, fullname: str, source):
        super().__init__(fullname, source)
        self.path = source

    def get_source(self, fullname: str) -> str | bytes:
        return self.path


class ApiMiddlewareManager:
    repo: FileRepository = None
    store: AppStore = None
    sections: GenFileSections

    def __init__(self, sections: GenFileSections = AppFileSections):
        self.sections = sections

    async def _import_middleware(self, pl: ApiMiddleware):
        middlewares = await self.store.get_item("middleware") if await self.store.get_item("middleware") else []
        try:
            spec = spec_from_loader(pl.name, loader=SourceCodeLoader(pl.name, pl.source))
            pl.import_it(spec)
            if pl not in middlewares:
                middlewares.append(pl)
            await self.store.set_item("middleware", middlewares, send_event=False)
        except Exception as e:
            if settings.DEBUG:
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
            await self.store.set_item("middleware", middlewares, obj=True)
            return pl

    async def discover_middleware(self):
        for filename in await self.repo.open_section(self.sections.PLUGINS):
            await self._discover_middleware(filename)

    async def delete_middleware(self, filename: str):
        mdws = await self.store.get_item("middleware")
        new_mdws: List[ApiMiddleware] = []
        for mdw in mdws:
            if mdw.filename != filename:
                new_mdws.append(mdw)
        await self.store.set_item("middleware", new_mdws, obj=True)
        await self.import_middleware()

    async def add_new_middleware(self, filename: str):
        pl = await self._discover_middleware(filename)
        if pl:
            await self._import_middleware(pl)
            if settings.DEBUG:
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

    async def on_store_update(self, event: StoreUpdateEvent):
        if event.key == "middleware":
            await self.store.set_item("middleware", event.value, send_event=False)
            await self.import_middleware()

    def reg_channel_middleware(self):
        self.store.channel.add_event_middleware(StoreUpdateEvent.message_type, self.on_store_update)
        self.store.channel.add_event_middleware(StoreUpdateEvent.message_type, self.on_mdw_store_set,
                                                assign_to="before")

    async def on_mdw_store_set(self, event: StoreUpdateEvent):
        if event.key == "middleware":
            for mdw in event.value:
                mdw.imported = None
