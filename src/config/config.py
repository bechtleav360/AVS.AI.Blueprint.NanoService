import logging
import os

from dynaconf import Dynaconf


class ConfigurationManager:
    """Singleton Configuration class using dynaconf for using both default configurations and environment variables"""
    _settings = None
    _instance = None

    def __new__(cls):
        """Singleton Pattern"""

        if cls._instance is None:
            cls._instance = super(ConfigurationManager, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        self.logger = logging.getLogger("config")
        self.reload_config(os.path.join(os.getcwd(), "config", "config.json"))

    def reload_config(self, config_path: str):
        """Reload the config from the specified path"""

        self.logger.debug(f"Looking for config file in: {config_path}")
        self._settings: Dynaconf = Dynaconf(
            settings_files=[config_path, "settings.toml"],  # Specify the settings file
            merge_enabled=True
        )

    def get_config(self, json_path: str, default_value=None):
        """Get a configuration value from the config file"""

        self.logger.debug(f"Looking for config value: {json_path}")
        if self._settings is None:
            logging.getLogger("config").fatal("Config was not initialized before first use.")
            raise RuntimeError("Config not initialized")

        return self._settings(json_path, default_value)



