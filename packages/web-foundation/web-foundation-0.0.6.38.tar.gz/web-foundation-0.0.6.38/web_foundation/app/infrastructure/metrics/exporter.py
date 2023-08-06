from typing import List, Generic, Dict

from web_foundation.app.infrastructure.metrics.formatter import GenMetricFormatter, JsonMetricFormatter, \
    GenericMetricFormat
from web_foundation.app.infrastructure.metrics.metric import Metric


class MetricExporter(Generic[GenMetricFormatter]):
    _formatter: GenMetricFormatter = JsonMetricFormatter[Dict]

    def _generate_response(self, data: List[GenericMetricFormat]):
        return data

    def generate_response(self, metrics: List[Metric]):
        self._generate_response(self.export(metrics))

    def export(self, metrics: List[Metric]) -> List[GenericMetricFormat]:
        formatted_: List[GenericMetricFormat] = []
        for metric in metrics:
            if not isinstance(metric, list):
                formatted_.append(self._formatter.format_by_one(metric))
            else:
                formatted_.append(self._formatter.format_many_one_type(metric))
        return formatted_

    def empty(self):
        return self._formatter.empty()
