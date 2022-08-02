import configparser


class AppConfig:
    def __init__(self):
        self.config = configparser.ConfigParser()
        self.config.read("resources/config.cfg")

    def get(self, config_type: str, key: str) -> object:
        return self.config[config_type].get(key)

    def set(self, config_type: str, key: str, value: str) -> None:
        self.config.set(config_type, key, value)
