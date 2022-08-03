import configparser


class AppConfig:
    def __init__(self):
        self.config = configparser.ConfigParser()
        self.path = "resources/config.cfg"
        self.config.read(self.path)

    def get(self, config_type: str, key: str) -> object:
        self.config.read(self.path)
        return self.config[config_type].get(key)

    def set(self, config_type: str, key: str, value: str) -> None:
        self.config.set(config_type, key, value)
        with open(self.path, "w") as configfile:
            self.config.write(configfile)