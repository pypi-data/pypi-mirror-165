from typing import List, Dict, Any

from web_foundation.app.infrastructure.metrics.basemetric import BaseMetric
from web_foundation.app.resources.stores.store import TypeJSON


class MetricExporter:
    @classmethod
    def export(cls, metrics: List[BaseMetric]) -> Dict[str, Any]:
        raise NotImplementedError

    @classmethod
    def empty(cls):
        return {}


class JsonExporter(MetricExporter):
    @classmethod
    def export(cls, metrics: List[BaseMetric]) -> Dict[str, TypeJSON]:
        dic = {}
        for metric in metrics:
            if not metric:
                continue
            if not dic.get(metric.name):
                dic[metric.name] = [{"value": metric.collect(),
                                     "labels": metric.labels,
                                     "timestamp": metric.timestamp}]
            else:
                dic[metric.name].append({"value": metric.collect(),
                                         "labels": metric.labels,
                                         "timestamp": metric.timestamp})
        return dic


class PrometheusExporter(MetricExporter):
    @classmethod
    def export(cls, exprot_metrics: List[BaseMetric]) -> Dict[str, Any]:
        try:
            from prometheus_client import metrics, registry
        except ImportError:
            raise ImportError(
                "You need to install prometheus-client to use PrometheusExporter (web-foundation[prometheus])")
