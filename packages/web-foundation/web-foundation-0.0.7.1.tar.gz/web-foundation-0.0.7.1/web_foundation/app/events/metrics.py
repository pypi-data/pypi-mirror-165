from typing import Set, List

from web_foundation.app.infrastructure.metrics.exporter import Metric
from web_foundation.kernel import IMessage


class NewMetricEvent(IMessage):
    message_type = "new_metric"
    destination = "__dispatcher__"
    metric: Metric

    def __init__(self, metric: Metric):
        super().__init__()
        self.metric = metric

    def __str__(self):
        return f"NewMetricEvent({self.metric.__str__()})"


class MetricRequest(IMessage):
    message_type = "metrics_request"
    destination = "__dispatcher__"


class MetricResponse(IMessage):
    message_type = "metrics_response"
    metrics: List[Metric]

    def __init__(self, metrics: List[Metric]):
        super().__init__()
        self.metrics = metrics

    def __str__(self):
        return f"MetricResponse({[met.__str__() for met in self.metrics]})"
