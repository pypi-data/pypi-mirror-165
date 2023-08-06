from typing import Any, Dict, Optional

from dependency_injector.resources import T
from loguru import logger

from web_foundation.app.resources.stores.store import AppStore
from web_foundation import settings


class InMemoryDictStore(AppStore):
    need_sync = True
    _storage: Dict

    def __init__(self, *args, **kwargs):
        self._storage = {}

    async def _set_item(self, key: str, value: Any):
        if settings.DEBUG:
            if self._storage.get(key):
                logger.debug(f"the key ({key}) will be overwritten")
        self._storage[key] = value

    async def get_item(self, key: str) -> Any:
        ret_val = self._storage.get(key)
        if settings.DEBUG and not ret_val:
            logger.debug(f"""Can"t find key "{key}" in store""")
        return ret_val

    async def size(self):
        return len(self._storage)

    async def get_all(self):
        return self._storage.items()
