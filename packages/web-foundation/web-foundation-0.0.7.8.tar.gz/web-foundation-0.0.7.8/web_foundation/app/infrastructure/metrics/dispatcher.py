from typing import Dict

import loguru

from web_foundation import settings
from web_foundation.app.events.metrics import NewMetricEvent, MetricRequest, MetricResponse
from web_foundation.app.infrastructure.metrics.basemetric import CounterBaseMetric
from web_foundation.app.infrastructure.metrics.exporter import BaseMetric
from web_foundation.kernel import GenericIMessage
from web_foundation.kernel.dispatcher import IDispatcher

if settings.METRICS_ENABLE:
    try:
        from prometheus_client.metrics import Gauge, Histogram, Counter, MetricWrapperBase
    except ImportError:
        settings.PROMETHEUS_METRICS_ENABLE = False


class MetricsDispatcher(IDispatcher):
    collected_metrics: Dict[str, Dict[str, BaseMetric]]

    def __init__(self):
        super().__init__()
        self.collected_metrics = {}
        self.add_event_listener(NewMetricEvent.message_type, self.on_new_metric)
        self.add_event_listener(MetricRequest.message_type, self.on_metric_request)

    async def on_metric_request(self, event: MetricRequest):
        exporter = event.exporter
        sender_channel = self.channels.get(event.sender)
        if sender_channel:
            if settings.DEBUG:
                loguru.logger.debug(f"Send METRICS to {sender_channel}")
            if not self.collected_metrics:
                await sender_channel.sent_to_consume(exporter.empty())
            rp = []
            for i in self.collected_metrics.values():
                if isinstance(i, dict):
                    for k in i.values():
                        rp.append(k)
                else:
                    rp.append(i)
            resp = MetricResponse(exporter.export(rp))
            resp.inner_index = event.inner_index
            await sender_channel.sent_to_consume(resp)

    async def on_new_metric(self, event: NewMetricEvent):
        metr = self.collected_metrics.get(event.metric.name)
        if not metr:
            self.collected_metrics.update({event.metric.name: {event.metric.labels_concat: event.metric}})
        else:
            if metr.get(event.metric.labels_concat):
                # loguru.logger.warning(f"get {event.metric}")
                metr[event.metric.labels_concat] += event.metric
            else:
                # loguru.logger.warning(f"set {event.metric}")
                metr[event.metric.labels_concat] = event.metric

    async def track_event(self, msg: GenericIMessage):
        await super(MetricsDispatcher, self).track_event(msg)
        if settings.EVENTS_METRIC_ENABLE:
            event_counter = CounterBaseMetric("events_counter", self._msg_global_index)
            self.collected_metrics.update({"events_counter": {"dispatcher_events_counter": event_counter}})

            named_event_counter = self.collected_metrics.get("named_events_counter")
            if not named_event_counter:
                mtr = CounterBaseMetric("named_events_counter", value=1)
                mtr.add_label(event_name=msg.message_type)
                named_event_counter = {msg.message_type: mtr}
                self.collected_metrics["named_events_counter"] = named_event_counter
            elif named_event_counter.get(msg.message_type):
                named_event_counter[msg.message_type].inc()
            else:
                mtr = CounterBaseMetric("named_events_counter", value=1)
                mtr.add_label(event_name=msg.message_type)
                named_event_counter[msg.message_type] = mtr
            if settings.DEBUG:
                loguru.logger.debug(f'MetricsDispatcher - track event {msg}')
