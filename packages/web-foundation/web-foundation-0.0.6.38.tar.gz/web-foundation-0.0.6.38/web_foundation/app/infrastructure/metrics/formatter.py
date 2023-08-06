from web_foundation.app.infrastructure.metrics.metric import Metric
from typing import TypeVar, Generic, List, Dict

GenericMetricFormat = TypeVar("GenericMetricFormat")


class MetricFormatter(Generic[GenericMetricFormat]):

    @classmethod
    def format_by_one(cls, metric: Metric) -> GenericMetricFormat:
        raise NotImplementedError

    @classmethod
    def empty(cls) -> GenericMetricFormat:
        raise NotImplementedError


class JsonMetricFormatter(MetricFormatter, Generic[GenericMetricFormat]):

    @classmethod
    def empty(cls) -> GenericMetricFormat:
        return {}

    @classmethod
    def format_by_one(cls, metric: Metric) -> GenericMetricFormat:
        return {"name": metric.name,
                "value": metric.value,
                "labels": metric.labels,
                "timestamp": metric.timestamp}

    @classmethod
    def format_many_one_type(cls, metrics: List[Metric]) -> GenericMetricFormat:
        return {"name": metrics[0].name, "metrics": [cls.format_by_one(m) for m in metrics]}


GenMetricFormatter = TypeVar("GenMetricFormatter", bound=MetricFormatter, contravariant=True)
