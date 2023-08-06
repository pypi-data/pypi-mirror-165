from typing import Generic

from web_foundation.kernel import IMessage
from web_foundation.app.events.background_task import BgTask, TaskIMessage
from web_foundation.workers.worker import GenWorker


class Service(Generic[GenWorker]):
    _worker: GenWorker

    async def run_background(self, task: BgTask, *args, **kwargs):
        await self._worker.channel.produce(
            TaskIMessage(task, args=args, kwargs=kwargs)
        )

    async def wait_for_response(self, msg: IMessage):
        return await self.worker.channel.produce_for_response(msg)

    @property
    def worker(self) -> GenWorker:
        return self._worker

    @worker.setter
    def worker(self, worker: GenWorker):
        self._worker = worker

    async def emmit_event(self, event: IMessage):
        await self._worker.channel.produce(event)

    # async def microtask(self, task: Coroutine):
    #     return asyncio.create_task(task)
