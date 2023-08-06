import asyncio
import time
from types import SimpleNamespace
from typing import List, Dict

from loguru import logger
from sanic import Sanic, Request
from sanic.response import BaseHTTPResponse

from web_foundation import settings
from web_foundation.app.events.metrics import NewMetricEvent
from web_foundation.app.infrastructure.metrics.exporter import Metric, MetricExporter
from web_foundation.app.infrastructure.metrics.formatter import GenMetricFormatter
from web_foundation.kernel import IChannel
from web_foundation import settings


class MetricsMixin:
    _metrics: List[Metric]
    _channel: IChannel

    def _reg_metrics(self):
        pass

    async def give_metric(self, metric: Metric):
        if settings.METRICS.get(metric.name):
            asyncio.create_task(self._channel.produce(NewMetricEvent(metric)))
        else:
            if settings.DEBUG:
                logger.debug(f"Metric({metric.name}) not enable in settings.METRIC")


class ApiMetricsMixin(MetricsMixin):
    app_name: str
    sanic_app: Sanic
    stored_metric: Dict[str, Metric] = {
        "request_path_count": Metric("request_path_count", 0),
        "request_exec_time_long": Metric("request_exec_time", long=True)
    }

    def _reg_metrics(self):
        async def metrics_before(request: Request):
            if not settings.METRICS_ENABLE:
                return
            request.ctx.metrics = SimpleNamespace()
            if settings.METRICS.get("request_path_count"):
                metr = self.stored_metric.get("request_path_count")
                metr.add_labels(request.path)
                metr.add_labels(request.method)
                metr.value += 1
                await self.give_metric(metr)
            if settings.METRICS.get("request_exec_time"):
                request.ctx.metrics.exec_time = time.time()

        async def metrics_after(request: Request, response: BaseHTTPResponse):
            if not settings.METRICS_ENABLE:
                return
            if settings.METRICS.get("request_exec_time"):
                metr = self.stored_metric.get("request_exec_time_long")
                metr.value = time.time() - request.ctx.metrics.exec_time
                metr.add_labels([request.path, request.method, str(response.status)])
                await self.give_metric(metr)

        self.sanic_app.register_middleware(metrics_before)
        self.sanic_app.register_middleware(metrics_after, "response")
