from typing import List, Set, Tuple, Sequence, Union, Dict
from datetime import datetime
from timeit import default_timer


class MetricTimer:
    def __init__(self, metric, callback):
        self._metric = metric
        self._callback = callback

    def __enter__(self):
        self._start = default_timer()
        return self

    def __exit__(self, typ, value, traceback):
        # Time can go backwards.
        duration = max(default_timer() - self._start, 0)
        self._callback(duration)


class BaseMetric:
    name: str
    value: float
    labels: Dict[str, str]
    timestamp: float

    def __init__(self, name: str, value: float = 0.0, labels: Dict[str, str] = None):
        self.labels = labels if labels else {}
        self.timestamp = datetime.now().timestamp()
        self.name = name
        self.value = float(value)

    def add_label(self, name: str = None, value: str = None, **kwargs):
        if kwargs:
            self.labels.update(kwargs)
        else:
            self.labels.update({name: value})

    def set(self, value: float):
        self.value = value

    @property
    def labels_concat(self):
        return '_'.join(self.labels.values())

    def __str__(self):
        return f"Metric({self.name})<{self.value}>"

    def __repr__(self):
        return f"Metric({self.name})<{self.value}>"

    def __eq__(self, other):
        return self.name == other.name

    def __hash__(self):
        return id(self.name)


class CounterBaseMetric(BaseMetric):

    def inc(self):
        self.value += 1


class GaugeBaseMetric(BaseMetric):

    def inc(self):
        self.value += 1

    def dec(self):
        self.value -= 1

    def set(self, value: float):
        self.value = value


class SummaryBaseMetric(BaseMetric):
    _count: int = 0
    _sum: float = 0.0

    def observe(self, amount: float) -> None:
        """Observe the given amount.
        The amount is usually positive or zero. Negative values are
        accepted but prevent current versions of Prometheus from
        properly detecting counter resets in the sum of
        observations. See
        https://prometheus.io/docs/practices/histograms/#count-and-sum-of-observations
        for details.
        """
        self._count += 1
        self._sum += amount

    def time(self) -> MetricTimer:
        """Time a block of code or function, and observe the duration in seconds.
        Can be used as a function decorator or context manager.
        """
        return MetricTimer(self, self.observe)


class HistogramBaseMetric(BaseMetric):
    _sum: float = 0.0
    _buckets: List[Tuple[float, float]]
    _temp_bucket: Sequence[Union[float, str]]
    DEFAULT_BUCKETS = (.005, .01, .025, .05, .075, .1, .25, .5, .75, 1.0, 2.5, 5.0, 7.5, 10.0, float("inf"))

    def __init__(self, name: str):

        super().__init__(name)
        self._temp_bucket = self.DEFAULT_BUCKETS

    def set_bucket(self, buckets: Sequence[Union[float, str]]):
        buckets = [float(b) for b in buckets]
        if buckets != sorted(buckets):
            raise ValueError('Buckets not in sorted order')
        if buckets and buckets[-1] != float("inf"):
            buckets.append(float("inf"))
        if len(buckets) < 2:
            raise ValueError('Must have at least two buckets')

    def observe(self, amount: float) -> None:
        """Observe the given amount.
        The amount is usually positive or zero. Negative values are
        accepted but prevent current versions of Prometheus from
        properly detecting counter resets in the sum of
        observations. See
        https://prometheus.io/docs/practices/histograms/#count-and-sum-of-observations
        for details.
        """
        self._sum += amount
        for i, bound in enumerate(self._temp_bucket):
            if amount <= bound:
                self._buckets[i] += 1

    def time(self) -> MetricTimer:
        """Time a block of code or function, and observe the duration in seconds.
        Can be used as a function decorator or context manager.
        """
        return MetricTimer(self, self.observe)
