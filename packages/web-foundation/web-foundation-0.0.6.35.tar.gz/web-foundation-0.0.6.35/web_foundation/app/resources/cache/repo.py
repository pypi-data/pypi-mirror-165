from typing import Any


class AppStore:
    debug: bool = False
    need_sync = False

    def __init__(self, debug: bool = False):
        self.debug = debug

    async def get_item(self, key: str) -> Any:
        raise NotImplementedError

    async def set_item(self, key: str, value: Any):
        raise NotImplementedError

    async def get_all(self):
        raise NotImplementedError

    async def size(self):
        raise NotImplementedError
