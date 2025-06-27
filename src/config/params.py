from enum import Enum


class ConfigParameter(Enum):
    APP_NAME = "app_name"
    APP_DESCRIPTION = "app_description"
    APP_PORT = "app_port"
    APP_VERSION = "app_version"
    APP_ENVIRONMENT = "app_environment"
    APP_URL_PREFIX = "app_url_prefix"
    LOG_LEVEL = "log_level"
    LOG_FILE = "log_file"
    LOG_LOGGER_NAMES = "log_logger_names"
    LOG_LOGGER_LEVEL = "log_logger_level"

    # extend parameters here (don't forget to add them to config.json)
