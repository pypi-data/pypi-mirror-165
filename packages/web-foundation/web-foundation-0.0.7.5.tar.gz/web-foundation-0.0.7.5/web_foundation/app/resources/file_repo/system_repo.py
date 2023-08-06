import os.path
from enum import Enum
from pathlib import Path
from typing import Type, Any, List, Optional

from aiofiles import open
from aiofiles.base import AiofilesContextManager
from dependency_injector.resources import T
from loguru import logger

from web_foundation.app.errors.io.files import SectionNotFound, FileNotExist, NothingToWrite, OsIOError, \
    NestedFolderDetected
from web_foundation.app.resources.file_repo.repo import FileRepository, AppFileSections, GenFileSections
from web_foundation import settings


class SystemFileRepository(FileRepository):
    _root: Path

    def __init__(self, root: Path, sections: GenFileSections = AppFileSections):
        super(SystemFileRepository, self).__init__(sections)
        self._root = root
        self._sections = sections
        self._create_sections()

    def _create_sections(self):
        for section in self._sections:
            folder = os.path.join(self._root, str(section.value))
            if not self._check_exist(folder, raises=False):
                os.mkdir(folder)

    def _check_exist(self, path: str, raises: bool = True) -> bool:
        exist = os.path.exists(path)
        if not exist and raises:
            raise FileNotExist(message=f"File not exists in path {path}")
        return exist

    def _get_full_path(self, filename: str, section: GenFileSections):
        if section not in self._sections:
            raise SectionNotFound(message=f"Not found {section} in {self._sections}")
        full_path = os.path.join(self._root, str(section.value), filename)
        return full_path

    def _check_full_path(self, filename: str, section: GenFileSections, raises: bool = True):
        full_path = self._get_full_path(filename, section)
        self._check_exist(full_path, raises=raises)
        if os.path.isdir(full_path) and raises:
            raise NestedFolderDetected(message=f"{full_path} is dir")
        return full_path

    # overload
    async def _open_section(self, section: GenFileSections) -> List[str]:
        path = os.path.join(self._root, str(section.value))
        self._check_exist(path)
        filenames = []
        for inner_path in os.listdir(path):
            if os.path.isdir(os.path.join(path, inner_path)):
                continue
            filenames.append(inner_path)
        return filenames

    # overload
    async def stash(self, filename: str, section: GenFileSections, data: Any, raises: bool = True, **kwargs) -> None:
        if not data:
            raise NothingToWrite(message="No data to write")
        try:
            full_path = self._get_full_path(filename, section)  # TODO create dirs if "/" in filename?
            async with open(full_path, **kwargs) as target_file:
                await target_file.write(data)
        except Exception as e:
            if settings.DEBUG:
                logger.debug(f"File write error {e}")
            if raises:
                raise OsIOError(message="Can't write to file", ex=e)

    # overload
    async def take(self, filename: str, section: GenFileSections, raises: bool = True,
                   **kwargs) -> AiofilesContextManager | None:
        try:
            full_path = self._check_full_path(filename, section, raises=raises)
            return open(full_path, **kwargs)
        except Exception as e:
            if settings.DEBUG:
                logger.debug(f"File open error {e}")
            if raises:
                raise OsIOError(message="Can't open file", ex=e)
            return None

    async def get_file_fullpath(self, filename: str, section: Enum) -> str:
        pass
