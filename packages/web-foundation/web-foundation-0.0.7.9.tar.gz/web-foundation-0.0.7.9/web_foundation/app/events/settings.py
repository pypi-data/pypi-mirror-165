from web_foundation.kernel import IMessage


class SettingsChange(IMessage):
    message_type = "change_settings_event"
    name: str
    value: bool

    def __init__(self, name: str, value: bool):
        super().__init__()
        self.name = name
        self.value = value

    def __str__(self):
        return f"{self.__class__.__name__}({self.name})"
