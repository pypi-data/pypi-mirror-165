from typing import Any

from web_foundation.kernel import IMessage


class StoredApiMdwNew(IMessage):
    message_type = "store_api_mdw_new"
    filename: str

    def __init__(self, filename: str):
        super().__init__()
        self.filename = filename


class StoredApiMdwDelete(IMessage):
    message_type = "store_api_mdw_delete"
    filename: str

    def __init__(self, filename: str):
        super().__init__()
        self.filename = filename


class StoreUpdateEvent(IMessage):
    message_type = "store_update"

    def __init__(self, key: str, value: Any):
        super().__init__()
        self.key = key
        self.value = value

    def __str__(self):
        return f"{self.__class__.__name__}({self.key})"
