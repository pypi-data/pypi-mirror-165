from typing import Any, Dict
from loguru import logger

from web_foundation.app.resources.cache.repo import AppStore


class InMemoryDictStore(Dict, AppStore):
    need_sync = True

    async def set_item(self, key: str, value: Any):
        if self.debug:
            if self.get(key):
                logger.debug(f"the key ({key}) will be overwritten")
        self[key] = value

    async def get_item(self, key: str) -> Any:
        ret_val = self.get(key)
        if self.debug and not ret_val:
            logger.debug(f"Can't find key {key} in store")
        return ret_val

    async def size(self):
        return len(self)

    async def get_all(self):
        return self.items()
