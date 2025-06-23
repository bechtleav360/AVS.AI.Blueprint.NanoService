import logging

from src.config.config import ConfigurationManager

SETTINGS = ConfigurationManager()


# TODO Better Logging
def configure() -> None:
    """Configure global logging settings"""
    try:
        # Configure basic logging with console and file output
        logging_file_handler = logging.FileHandler(SETTINGS.get_config("log_file"))
        log_message_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        log_date_format = '%Y-%m-%dT%H:%M:%S'
        logging_file_handler.setFormatter(logging.Formatter(log_message_format,datefmt=log_date_format))
        # Configure basic logging with console and file output
        logging.basicConfig(
            # Set the global logging level (DEBUG, INFO, etc.)
            level=SETTINGS.get_config("log_level"),
            # Log message format
            format=log_message_format,
            # ISO 8601 Date format
            datefmt=log_date_format,
            handlers=[
                # Console handler
                logging.StreamHandler(),
                # File handler
                logging_file_handler
            ]
        )
        
        # Set specific loggers to INFO level
        loggers = [
            "api",
            "httpx", 
            "twisted",
            "asyncio",
            "httpcore",
            "werkzeug"
        ]
        
        for logger_name in loggers:
            try:
                logging.getLogger(logger_name).setLevel(level=SETTINGS.get_config("log_level"))
                logging.getLogger(logger_name).addHandler(logging_file_handler)
            except Exception as e:
                logging.error(f"Failed to configure logger '{logger_name}': {repr(e)}")
                
    except Exception as e:
        # If basic config fails, log error and use default logging config
        print(f"Failed to configure logging: {repr(e)}")
        logging.basicConfig(level=logging.INFO)        
