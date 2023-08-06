from typing import List, Set
from datetime import datetime


class Metric:
    name: str
    value: float
    labels: List[str]
    timestamp: float
    long: bool

    def __init__(self, name: str, value: float = 0.0, labels: List[str] | str = None, long: bool = False):
        self.labels = labels if labels else []
        self.timestamp = datetime.now().timestamp()
        self.name = name
        self.value = float(value)
        self.long = long

    def add_labels(self, labels: List[str] | str):
        if isinstance(labels, list):
            for i in labels:
                self.labels.append(i)
        else:
            self.labels.append(labels)

    def set(self, value: float):
        self.value = value

    def __str__(self):
        return f"Metric({self.name})<{self.value}> {self.long=}"

    def __repr__(self):
        return f"Metric({self.name})<{self.value}> {self.long=}"

    def __eq__(self, other):
        return self.name == other.name

    def __hash__(self):
        return id(self.name)


# class LongMetric(Metric):
#     value: List[Metric]
#
#     def __init__(self, name: str):
#         super().__init__(name)
#         self.value = []
#
#     def add(self, value: Metric):
#         self.value.append(value)
#
#     def __str__(self):
#         return f"LongMetric({self.name})<{len(self.value)},{self.value[-1].value}>"
#
#     def __repr__(self):
#         return f"LongMetric({self.name})<{len(self.value)},{self.value[-1].value}>"
