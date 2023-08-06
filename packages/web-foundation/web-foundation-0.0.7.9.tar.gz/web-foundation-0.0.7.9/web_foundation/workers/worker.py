from __future__ import annotations

from typing import TypeVar

from dependency_injector import containers
from dependency_injector.wiring import inject, Provide

from web_foundation import settings
from web_foundation.app.events.settings import SettingsChange
from web_foundation.app.resources.file_repo.repo import FileRepository
from web_foundation.app.resources.stores.store import AppStore
from web_foundation.kernel import Isolate


class Worker(Isolate):
    app_name: str
    _configured: bool
    _store: AppStore | None = None
    _repo: FileRepository | None = None

    def __init__(self, *args, **kwargs):
        self._configured = False

    @property
    def configured(self) -> bool:
        return self._configured

    @inject
    async def _init_resources(self, *args, app_container=Provide["<container>"], **kwargs):
        init_coro = app_container.init_resources()
        if init_coro:
            await init_coro
        for service in app_container.app().services.values():
            service.worker = self

    async def on_settings_change(self, event: SettingsChange):
        setattr(settings, event.name, event.value)

    def configure(self, name: str, *args, **kwargs):
        self._configure_isolate(name)
        self._configure(*args, **kwargs)
        self.channel.add_event_listener(SettingsChange, self.on_settings_change)
        self._configured = True

    def post_configure(self):
        self._reg_metrics()
        self._post_configure()

    def _post_configure(self):
        raise NotImplementedError

    def _configure(self, *args, **kwargs):
        pass

    def wire_worker(self, container: containers.DeclarativeContainer) -> None:
        raise NotImplementedError

    async def _run(self):
        raise NotImplementedError

    def _close(self):
        pass

    @property
    def store(self):
        return self._store

    @store.setter
    def store(self, store: AppStore):
        store.channel = self.channel
        self._store = store

    @property
    def repo(self):
        return self._repo

    @repo.setter
    def repo(self, value: FileRepository):
        self._repo = value


GenWorker = TypeVar("GenWorker", bound=Worker)
