import asyncio
from asyncio import Future
from typing import Dict, List, Any

import loguru

from web_foundation import settings
from web_foundation.kernel import IChannel, GenericIMessage, EventListener
from web_foundation.workers.worker import GenWorker


class IDispatcher:
    channels: Dict[str, IChannel]
    events_listeners: Dict[str, EventListener]
    _msg_global_index: int

    def __init__(self):
        self._msg_global_index = 0
        self.channels = {}
        self.events_listeners = {}

    def reg_worker(self, worker: GenWorker):
        self.channels.update({worker.name: worker.channel})

    def add_event_listener(self, event_type: str, callback: EventListener):
        self.events_listeners[event_type] = callback

    async def track_event(self, msg: GenericIMessage):
        listener = self.events_listeners.get(msg.message_type)
        if listener:
            await listener(msg)

    async def on_channel_sent(self, msg: GenericIMessage):
        self._msg_global_index += 1
        msg.index = self._msg_global_index
        asyncio.create_task(self.track_event(msg))
        if msg.destination != "__dispatcher__":
            asyncio.create_task(self.broadcast(msg))

    async def broadcast(self, msg: GenericIMessage):
        for worker_name, ch in self.channels.items():
            if msg.sender == worker_name:
                continue
            if msg.destination in ["__all__", worker_name]:
                if settings.DEBUG:
                    loguru.logger.debug(f"Sent {msg} to {ch.worker_name}")
                await ch.consume_pipe.write(msg)

    def preform(self) -> List[Future[Any]]:
        tasks = []
        for channel in self.channels.values():
            tasks.append(asyncio.ensure_future(
                channel.listen_produce(
                    self.on_channel_sent
                )))
        return tasks
