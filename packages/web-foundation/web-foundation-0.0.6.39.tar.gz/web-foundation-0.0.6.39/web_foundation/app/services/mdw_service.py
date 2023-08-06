from web_foundation.app.services.service import Service


class ApiMiddlewareService(Service):


    async def add_new_middleware(self, filename: str):
        await self._worker.mdw_manager.add_new_middleware(filename)

    async def delete_middleware(self, filename: str):
        await self._worker.mdw_manager.delete_middleware(filename)
