import logging
import os
from typing import List, Optional

from dynaconf import Dynaconf  # type: ignore[import]

from .params import ConfigParameter


class ConfigurationManager:
    """
    Configuration class using dynaconf for using both default configurations and environment variables.
    Also handles logging configuration.
    """

    def __init__(self, config_path: Optional[str] = None):
        """Initialize the configuration manager.

        Args:
            config_path: Optional path to the configuration file. If not provided,
                       will look for 'config/config.json' in the current working directory.
        """
        self._settings = None
        self._log_handlers: List[logging.Handler] = []
        self.logger = logging.getLogger("config")
        self._valid = True
        self._reason = ""

        if config_path is None:
            config_path = os.path.join(os.getcwd(), "config", "config.json")

        self.reload_config(config_path)
        self._setup_logging()

    def invalidate(self, reason: str) -> None:
        """
        Invalidate the configuration with a specific reason. Once you marked the configuration as invalid, the
        shealth/ready checks will fail.

        Args:
            reason: The reason for invalidation
        """
        self._valid = False
        self._reason = reason

    def is_valid(self) -> bool:
        """
        Check if the configuration is valid.

        Returns:
            True if the configuration is valid, False otherwise
        """
        return self._valid

    def get_reason(self) -> str:
        """
        Get the reason for invalidation.

        Returns:
            The reason for invalidation
        """
        return self._reason

    def reload_config(self, config_path: str) -> None:
        """Reload the config from the specified path"""
        self.logger.debug(f"Looking for config file in: {config_path}")
        self._settings = Dynaconf(
            settings_files=[config_path, "settings.toml"],
            merge_enabled=True,
        )
        self._setup_logging()

    def get_config(self, key: str | ConfigParameter, default_value=None):
        """Get a configuration value from the config file"""
        self.logger.debug(f"Looking for config value: {key}")

        if not self.is_valid():
            self.logger.fatal("Config is invalid. Reason: %s", self.get_reason())
            raise RuntimeError("Config is invalid")

        if self._settings is None:
            self.logger.fatal("Config was not initialized before first use.")
            raise RuntimeError("Config not initialized")

        if isinstance(key, ConfigParameter):
            key = key.value

        return self._settings(key, default_value)

    def _setup_logging(self) -> None:
        """Configure logging based on the current configuration"""
        try:
            log_level = self.get_config(ConfigParameter.LOG_LEVEL, "INFO").upper()
            log_file = self.get_config(ConfigParameter.LOG_FILE, "app.log")
            log_message_format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
            log_date_format = "%Y-%m-%dT%H:%M:%S"

            # Clear existing handlers
            for handler in self._log_handlers:
                try:
                    handler.close()
                except Exception as e:
                    print(f"Error closing log handler: {e}")
            self._log_handlers = []

            # Configure file handler
            file_handler = logging.FileHandler(log_file)
            file_handler.setFormatter(
                logging.Formatter(log_message_format, datefmt=log_date_format)
            )
            self._log_handlers.append(file_handler)

            # Configure console handler
            console_handler = logging.StreamHandler()
            console_handler.setFormatter(
                logging.Formatter(log_message_format, datefmt=log_date_format)
            )
            self._log_handlers.append(console_handler)

            # Get logger names to configure
            loggers = self.get_config(
                ConfigParameter.LOG_LOGGER_NAMES,
                ["api", "httpx", "twisted", "asyncio", "httpcore", "werkzeug"],
            )

            # Configure root logger with handlers and set level to WARNING to avoid double logging
            root_logger = logging.getLogger()
            root_logger.setLevel(logging.WARNING)  # Default to WARNING for root
            
            # Remove any existing handlers from root logger
            for handler in root_logger.handlers[:]:
                root_logger.removeHandler(handler)
            
            # Add our handlers to root logger
            for handler in self._log_handlers:
                root_logger.addHandler(handler)

            # Configure specific loggers with their levels and disable propagation
            for logger_name in loggers:
                try:
                    logger = logging.getLogger(logger_name)
                    logger.setLevel(
                        self.get_config(
                            ConfigParameter.LOG_LOGGER_LEVEL, log_level
                        ).upper()
                    )
                    # Disable propagation to prevent duplicate logs
                    logger.propagate = False
                    # Clear any existing handlers
                    for handler in logger.handlers[:]:
                        logger.removeHandler(handler)
                except Exception as e:
                    print(f"Failed to configure logger '{logger_name}': {e}")
                    continue
                
                # Add our handlers to this logger
                for handler in self._log_handlers:
                    logger.addHandler(handler)

        except Exception as e:
            print(f"Failed to configure logging: {e}")
            logging.basicConfig(level=logging.INFO)

    def get_log_level(self) -> int:
        """Get the current log level as a logging level constant"""
        level_str = self.get_config(ConfigParameter.LOG_LEVEL, "INFO").upper()
        return getattr(logging, level_str, logging.INFO)

    def get_log_file(self) -> str:
        """Get the configured log file path"""
        return self.get_config(ConfigParameter.LOG_FILE, "app.log")
