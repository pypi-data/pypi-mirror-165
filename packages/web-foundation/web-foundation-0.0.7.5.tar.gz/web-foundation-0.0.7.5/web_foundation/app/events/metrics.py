from typing import Any

from web_foundation.app.infrastructure.metrics.exporter import BaseMetric, MetricExporter
from web_foundation.kernel import IMessage


class NewMetricEvent(IMessage):
    message_type = "new_metric"
    destination = "__dispatcher__"
    metric: BaseMetric
    action: str

    def __init__(self, metric: BaseMetric, action: str = "inc"):
        super().__init__()
        self.metric = metric
        self.action = action

    def __str__(self):
        return f"NewMetricEvent({self.metric.__str__()})"


class MetricRequest(IMessage):
    message_type = "metrics_request"
    destination = "__dispatcher__"
    exporter: MetricExporter

    def __init__(self, exporter: MetricExporter):
        super().__init__()
        self.exporter = exporter


class MetricResponse(IMessage):
    message_type = "metrics_response"
    metrics_data: Any

    def __init__(self, metrics_data: Any):
        super().__init__()
        self.metrics_data = metrics_data

    def __str__(self):
        return f"MetricResponse({type(self.metrics_data)})"
