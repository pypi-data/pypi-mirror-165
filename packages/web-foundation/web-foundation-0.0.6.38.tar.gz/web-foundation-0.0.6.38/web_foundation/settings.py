from typing import Dict

DEBUG = False
LOG_LEVEL = 10
METRICS_ENABLE = False
EVENTS_METRIC_ENABLE = False
METRICS: Dict[str, bool] = {
    "request_path_count": True,
    "request_exec_time": True
}
