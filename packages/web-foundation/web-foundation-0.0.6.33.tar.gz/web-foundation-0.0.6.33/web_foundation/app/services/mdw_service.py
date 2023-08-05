from web_foundation.app.events.store import StoredPluginsUpdate
from web_foundation.app.services.service import Service


class ApiMiddlewareService(Service):

    def __init__(self):
        self._worker.channel.add_event_listener(StoredPluginsUpdate, self.on_plugin_store_update)
        pass

    async def on_plugin_store_update(self, event: StoredPluginsUpdate):
        await self._worker.mdw_manager.add_new_middleware(event.filename)

    async def add_new_middleware(self, filename: str):
        await self._worker.mdw_manager.add_new_middleware(filename)
        await self._worker.channel.produce(StoredPluginsUpdate(filename))
