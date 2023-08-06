import loguru

from web_foundation.app.events.metrics import MetricRequest, MetricResponse
from web_foundation.app.infrastructure.metrics.formatter import GenericMetricFormat
from web_foundation.app.services.service import Service


class MetricsService(Service):

    async def collect_metrics(self, formatter: GenericMetricFormat):
        metrics_response: MetricResponse = await self.wait_for_response(MetricRequest())
        exporter = self.worker.metrics_exporters.get(formatter)
        if not metrics_response or not metrics_response.metrics:
            return exporter.empty()
        return exporter.export(list(metrics_response.metrics))
