from typing import List, Dict, Any, AnyStr

from sanic.response import raw

from web_foundation.app.infrastructure.metrics.basemetric import BaseMetric, CounterBaseMetric, SummaryBaseMetric, \
    HistogramBaseMetric
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


def prometheus_response_fabric(data):
    return raw(data, content_type='text/plain; version=0.0.4; charset=utf-8')


class PrometheusExporter(MetricExporter):
    @classmethod
    def export(cls, export_metrics: List[BaseMetric]) -> AnyStr:
        try:
            from prometheus_client import metrics, registry
            from prometheus_client import metrics
            from prometheus_client.exposition import generate_latest
            from prometheus_client.metrics_core import CounterMetricFamily, \
                HistogramMetricFamily, \
                SummaryMetricFamily, \
                GaugeMetricFamily
            from prometheus_client.registry import Collector

            class CustomCollector(Collector):
                _custom_metrics: List[BaseMetric]

                def __init__(self, custom_metrics: List[BaseMetric]):
                    self._custom_metrics = custom_metrics

                def collect(self):
                    exp_metric = []
                    for metr in self._custom_metrics:
                        if isinstance(metr, CounterBaseMetric):
                            prm_metr = CounterMetricFamily(metr.name, metr.description, labels=metr.labels_keys)
                            prm_metr.add_metric(metr.labels_values, metr.value, timestamp=metr.timestamp)
                            yield prm_metr
                        elif isinstance(metr, SummaryBaseMetric):
                            prm_metr = SummaryMetricFamily(metr.name, metr.description, labels=metr.labels_keys)
                            prm_metr.add_metric(labels=metr.labels_values,
                                                sum_value=metr.value,
                                                count_value=metr.count,
                                                timestamp=metr.timestamp)
                            yield prm_metr
                        elif isinstance(metr, HistogramBaseMetric):
                            prm_metr = HistogramMetricFamily(metr.name, metr.description, labels=metr.labels_keys)
                            prm_metr.add_metric(labels=metr.labels_values,
                                                sum_value=metr.sum,
                                                buckets=metr.buckets_list,
                                                timestamp=metr.timestamp)
                            yield prm_metr
                    # value = CounterMetricFamily("SERVER_STATUS", 'Help text', labels='value')
                    # value.add_metric(["server_status"], server_status)
                    # yield exp_metric

            reg = registry.CollectorRegistry()
            reg.register(CustomCollector(export_metrics))
            return generate_latest(reg)
            # return  self._get_metrics_data()
        except ImportError:
            raise ImportError(
                "You need to install prometheus-client to use PrometheusExporter (web-foundation[prometheus])")
