from .base import BaseProcessor


class OptionsProcessor(BaseProcessor):
    def __init__(self, config_type: str, option_name: str, option_value: str) -> None:
        super().__init__()
        self.config_type = config_type
        self.option_name = option_name
        self.option_value = str(option_value)

    def process(self) -> None:
        self._config.set(self.config_type, self.option_name, self.option_value)
