from enum import Enum
from typing import Any, List, TypeVar, Generic

from aiofiles.base import AiofilesContextManager


class AppFileSections(Enum):
    CONFIG = "config"
    LOGS = "logs"
    PLUGINS = "plugins"
    MIGRATIONS = "migrations"


GenFileSections = TypeVar("GenFileSections", bound=AppFileSections)


class FileLoadContextManager:

    def __aenter__(self):
        raise NotImplementedError

    def __aexit__(self, exc_type, exc_val, exc_tb):
        raise NotImplementedError


class FileRepository(Generic[GenFileSections]):
    _sections: GenFileSections

    def __init__(self, sections: GenFileSections = AppFileSections):
        self._sections = sections

    async def stash(self, filename: str, section: GenFileSections, data: Any, raises: bool = True, **kwargs):
        raise NotImplementedError

    async def take(self, filename: str, section: GenFileSections, raises: bool = True,
                   **kwargs) -> AiofilesContextManager:
        raise NotImplementedError

    async def _open_section(self, section: GenFileSections) -> List[str]:
        raise NotImplementedError

    async def open_section(self, section: GenFileSections) -> List[str]:
        return await self._open_section(section)

    async def get_file_fullpath(self, filename: str, section: GenFileSections) -> str:
        raise NotImplementedError
