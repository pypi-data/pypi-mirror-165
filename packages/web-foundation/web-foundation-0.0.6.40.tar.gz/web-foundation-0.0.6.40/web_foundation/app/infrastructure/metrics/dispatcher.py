from typing import Set, Dict

import loguru

from web_foundation import settings
from web_foundation.app.events.metrics import NewMetricEvent, MetricRequest, MetricResponse
from web_foundation.app.infrastructure.metrics.exporter import Metric
from web_foundation.kernel import GenericIMessage
from web_foundation.kernel.dispatcher import IDispatcher


class MetricsDispatcher(IDispatcher):
    collected_metrics: Dict[str, Metric | list[Metric]]

    def __init__(self):
        super().__init__()
        self.collected_metrics = {}
        self.add_event_listener(NewMetricEvent.message_type, self.on_new_metric)
        self.add_event_listener(MetricRequest.message_type, self.on_metric_request)

    async def on_metric_request(self, event: MetricRequest):
        sender_channel = self.channels.get(event.sender)

        if sender_channel:
            if settings.DEBUG:
                loguru.logger.debug(f"Send METRICS to {sender_channel}")
            resp = MetricResponse(list(self.collected_metrics.values()))
            resp.inner_index = event.inner_index
            await sender_channel.sent_to_consume(resp)

    async def on_new_metric(self, event: NewMetricEvent):
        if event.metric.long:
            if not self.collected_metrics.get(event.metric.name):
                self.collected_metrics[event.metric.name] = [event.metric]
            else:
                self.collected_metrics[event.metric.name].append(event.metric)
        else:
            self.collected_metrics.update({event.metric.name: event.metric})

    async def track_event(self, msg: GenericIMessage):
        await super(MetricsDispatcher, self).track_event(msg)
        # TODO: create metric to track events
        if settings.EVENTS_METRIC_ENABLE:
            self.collected_metrics.update({"events_counter": Metric("events_counter", self._msg_global_index)})
            ev_counter_name = f"events_{msg.message_type}_counter"
            counter = self.collected_metrics.get(ev_counter_name)
            if not counter:
                self.collected_metrics[ev_counter_name] = Metric(ev_counter_name, 1)
            else:
                counter.value += 1
                self.collected_metrics[ev_counter_name] = counter
            if settings.DEBUG:
                loguru.logger.debug(f'MetricsDispatcher - track event {msg}')
