from enum import Enum

import loguru


class AppFileSections(Enum):
    CONFIG = "config"
    LOGS = "logs"
    PLUGINS = "plugins"
    MIGRATIONS = "migrations"


loguru.logger.warning(AppFileSections.PLUGINS in AppFileSections)