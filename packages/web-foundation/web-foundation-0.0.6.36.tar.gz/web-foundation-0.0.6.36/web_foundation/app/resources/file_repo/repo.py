from enum import Enum
from typing import Any, Type, List

from aiofiles.base import AiofilesContextManager


class AppFileSections(Enum):
    CONFIG = "config"
    LOGS = "logs"
    PLUGINS = "plugins"
    MIGRATIONS = "migrations"


class FileLoadContextManager:

    def __aenter__(self):
        raise NotImplementedError

    def __aexit__(self, exc_type, exc_val, exc_tb):
        raise NotImplementedError


class FileRepository:
    _sections: Type[Enum]
    debug: bool

    def __init__(self, sections: Type[Enum] = AppFileSections, debug: bool = False):
        self._sections = sections
        self.debug = debug

    async def stash(self, filename: str, section: Enum, data: Any, raises: bool = True, **kwargs):
        raise NotImplementedError

    async def take(self, filename: str, section: Enum, raises: bool = True,
                   **kwargs) -> AiofilesContextManager:
        raise NotImplementedError

    async def _open_section(self, section: Enum) -> List[str]:
        raise NotImplementedError

    async def open_section(self, section: Enum) -> List[str]:
        return await self._open_section(section)

    async def get_file_fullpath(self, filename: str, section: Enum) -> str:
        raise NotImplementedError
