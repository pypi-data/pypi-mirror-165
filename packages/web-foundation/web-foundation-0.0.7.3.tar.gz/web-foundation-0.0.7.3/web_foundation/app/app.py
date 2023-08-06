from __future__ import annotations

import asyncio
import json
from asyncio import Future
from pathlib import Path
from typing import List, Type, TypeVar, Generic, Dict, Any

from dependency_injector import providers, containers
from dependency_injector.wiring import inject, Provide
from pydantic import BaseSettings

from web_foundation import settings
from web_foundation.app.infrastructure.metrics.dispatcher import MetricsDispatcher
from web_foundation.app.resources.file_repo.repo import FileRepository
from web_foundation.app.resources.file_repo.system_repo import SystemFileRepository
from web_foundation.app.resources.stores.memory import InMemoryDictStore
from web_foundation.app.resources.stores.store import AppStore
from web_foundation.app.services.service import Service
from web_foundation.kernel.dispatcher import IDispatcher
from web_foundation.workers.worker import GenWorker

AppConfig = TypeVar("AppConfig", bound=BaseSettings)


class App(Generic[AppConfig, GenWorker]):
    config: AppConfig
    name: str
    workers: Dict[str, GenWorker]
    services: Dict[str, Service]
    dispatcher: IDispatcher
    store: AppStore
    repo: FileRepository = None

    # debug: bool  # type: ignore

    def __init__(self, config: providers.Configuration, store: AppStore = None, repo: FileRepository = None):
        self.name = config.get("app_name")
        self.store = store
        self.repo = repo
        self.config = config
        self.workers = {}
        self.services = {}
        self.dispatcher = MetricsDispatcher() if settings.METRICS_ENABLE else IDispatcher()

    @inject
    async def _before_app_run(self, app_container: AppContainer = Provide["<container>"]):
        init_coro = app_container.init_resources()
        if init_coro:
            await init_coro
        await self.before_app_run(app_container)

        shutdown_coro = app_container.shutdown_resources()
        if shutdown_coro:
            await shutdown_coro

    async def before_app_run(self, container):
        pass

    def _add_worker(self, worker: GenWorker):
        if not worker.configured:
            raise RuntimeError("Worker not configured")
        worker.store = self.store
        worker.repo = self.repo
        worker.app_name = self.name
        self.dispatcher.reg_worker(worker)
        worker.post_configure()
        self.workers.update({worker.name: worker})

    def add_worker(self, worker: GenWorker | List[GenWorker]):
        """
        Set isolate to app and set isolate debug and name
        :param worker: isolate to apply
        :return: None
        """
        if isinstance(worker, list):
            for w in worker:
                self._add_worker(w)
        else:
            self._add_worker(worker)

    def add_service(self, service: Service):
        self.services.update({service.__class__.__name__: service})

    def find_worker_by_pid(self, pid: int):
        for worker in self.workers.values():
            if worker.pid == pid:
                return worker

    def wire_app(self, container: AppContainer):
        container.wire(modules=[self.__module__])
        for worker in self.workers.values():
            container.wire(modules=[worker.__module__])
            worker.wire_worker(container)

    def perform(self) -> List[Future[Any]]:
        """
        Call performs from isolates and return all isolates Futures
        :return: None
        """
        return [worker.perform() for worker in self.workers.values()]

    async def run(self):
        await self._before_app_run()
        """
        Func to run app manually (without Runner)
        :return: None
        """
        return await asyncio.wait(self.perform() + self.dispatcher.preform())


def load_config(conf_path: Path, config_model: Type[AppConfig]) -> AppConfig:
    """
    Load app config to user in
    :param conf_path:
    :param config_model: BaseModel to cast json file to pydantic
    :return: None
    """
    with open(conf_path, "r") as _json_file:
        conf = config_model(**json.loads(_json_file.read()))
        return conf


class AppContainer(containers.DeclarativeContainer):
    app_config = providers.Configuration()
    store = providers.Dependency(instance_of=AppStore, default=providers.Singleton(InMemoryDictStore))
    file_repository = providers.Dependency(instance_of=FileRepository,
                                           default=providers.Singleton(SystemFileRepository,
                                                                       root=Path("applied_files")))
    app = providers.Dependency(instance_of=App,
                               default=providers.Singleton(App, config=app_config, store=store, repo=file_repository))
    """
    Please pass here your database or any another resource in nested container
    """
