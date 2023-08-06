from web_foundation.app.events.metrics import MetricRequest, MetricResponse
from web_foundation.app.infrastructure.metrics.basemetric import BaseMetric
from web_foundation.app.infrastructure.metrics.exporter import MetricExporter
from web_foundation.app.services.service import Service


class MetricsService(Service):

    async def collect_metrics(self, exporter: MetricExporter):
        metrics_response: MetricResponse = await self.wait_for_response(MetricRequest(exporter))
        return metrics_response.metrics_data

    async def give_metric(self, metric: BaseMetric):
        await self.worker.give_metric(metric)
