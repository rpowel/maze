import configparser

from common.path import get_resource_path


class AppConfig:
    def __init__(self):
        self.config = configparser.ConfigParser()
        self.path = get_resource_path("resources/user_config.cfg")
        self.default_path = get_resource_path("resources/default_config.cfg")
        self.config.read(self.path)

    def get(self, config_type: str, key: str) -> object:
        self.config.read(self.path)
        return self.config[config_type].get(key)

    def set(self, config_type: str, key: str, value: str) -> None:
        self.config.set(config_type, key, value)
        with open(self.path, "w") as configfile:
            self.config.write(configfile)

    def reset(self):
        self.config.read(self.default_path)
        with open(self.path, "w") as user_config:
            self.config.write(user_config)
