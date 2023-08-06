from copy import copy
from typing import Any, Union, Dict, List, Type

from orjson import dumps
from orjson import loads

from web_foundation.app.events.store import StoreUpdateEvent
from web_foundation.kernel import IChannel

JSON = Union[Dict[str, Any], List[Any], int, str, float, bool, Type[None]]
TypeJSON = Union[Dict[str, 'JSON'], List['JSON'], int, str, float, bool, Type[None]]


class AppStore:
    _channel: IChannel = None
    need_sync: bool = False

    async def on_store_update(self, event: StoreUpdateEvent):
        if not event.obj:
            event.value = self._load(event.value)
        await self.set_item(event.key, event.value, send_event=False)

    async def get_item(self, key: str) -> Any:
        raise NotImplementedError

    async def _set_item(self, key: str, value: TypeJSON):
        raise NotImplementedError

    async def set_item(self, key: str, value: Any, obj: bool = False, send_event: bool = True):
        await self._set_item(key, value)
        if self.need_sync and send_event:
            data = value if obj else self._serialize(value)
            await self._channel.produce(StoreUpdateEvent(key, copy(data), obj))

    async def get_all(self):
        raise NotImplementedError

    async def size(self):
        raise NotImplementedError

    def _load(self, value: str):
        return loads(value)

    def _serialize(self, value: TypeJSON):
        return dumps(value)

    @property
    def channel(self):
        return self._channel

    @channel.setter
    def channel(self, channel: IChannel):
        self._channel = channel
        if self.need_sync:
            self._channel.add_event_listener(StoreUpdateEvent, self.on_store_update)
