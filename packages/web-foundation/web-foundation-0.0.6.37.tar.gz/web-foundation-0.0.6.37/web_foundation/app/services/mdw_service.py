from web_foundation.app.events.store import StoredApiMdwNew, StoredApiMdwDelete
from web_foundation.app.services.service import Service


class ApiMiddlewareService(Service):

    def __init__(self):
        self._worker.channel.add_event_listener(StoredApiMdwNew, self.on_mdw_store_new)
        self._worker.channel.add_event_listener(StoredApiMdwDelete, self.on_mdw_store_delete)
        pass

    async def on_mdw_store_new(self, event: StoredApiMdwNew):
        await self._worker.mdw_manager.add_new_middleware(event.filename)

    async def on_mdw_store_delete(self, event: StoredApiMdwNew):
        await self._worker.mdw_manager.delete_middleware(event.filename)

    async def add_new_middleware(self, filename: str):
        await self._worker.mdw_manager.add_new_middleware(filename)
        await self._worker.channel.produce(StoredApiMdwNew(filename))

    async def delete_middleware(self, filename: str):
        await self._worker.mdw_manager.delete_middleware(filename)
        await self._worker.channel.produce(StoredApiMdwDelete(filename))
