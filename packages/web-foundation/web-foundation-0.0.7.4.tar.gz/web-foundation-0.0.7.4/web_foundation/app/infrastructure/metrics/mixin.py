import asyncio
import time
from types import SimpleNamespace
from typing import List, Dict

from sanic import Sanic, Request
from sanic.response import BaseHTTPResponse

from web_foundation import settings
from web_foundation.app.events.metrics import NewMetricEvent
from web_foundation.app.infrastructure.metrics.exporter import BaseMetric
from web_foundation.kernel import IChannel

# if settings.METRICS_ENABLE:
try:
    from prometheus_client.metrics import Gauge, Histogram, Counter, MetricWrapperBase
except ImportError:
    settings.PROMETHEUS_METRICS_ENABLE = False


class MetricsMixin:
    _metrics: List[BaseMetric]
    _channel: IChannel

    def _reg_metrics(self):
        pass

    async def give_metric(self, metric: BaseMetric, action: str = "inc"):
        asyncio.create_task(self._channel.produce(NewMetricEvent(metric, action)))


class ApiMetricsMixin(MetricsMixin):
    _name: str
    app_name: str
    sanic_app: Sanic
    stored_metric: Dict[str, BaseMetric]

    def _reg_metrics(self):
        self.sanic_app.ctx.metrics = SimpleNamespace()

        async def metrics_before(request: Request):
            if not settings.METRICS_ENABLE:
                return
            request.app.ctx.metrics.exec_time = time.time()

        async def metrics_after(request: Request, response: BaseHTTPResponse):
            if not settings.METRICS_ENABLE:
                return
            else:
                metr = BaseMetric(f"exec_request_time")
                metr.value = time.time() - request.app.ctx.metrics.exec_time
                metr.add_label(worker=self._name,
                               request=request.path,
                               method=request.method,
                               status=str(response.status))
                await self.give_metric(metr)
                metr = BaseMetric(f"request_path_count", value=1)
                metr.add_label(worker=self._name,
                               request=request.path,
                               method=request.method,
                               status=str(response.status))
                asyncio.create_task(self.give_metric(metr))

        self.sanic_app.register_middleware(metrics_before)
        self.sanic_app.register_middleware(metrics_after, "response")
