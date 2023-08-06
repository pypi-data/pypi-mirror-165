import os
import logging
from typing import Callable, Dict, Optional, Union, TypeVar
from logging.config import dictConfig

T = TypeVar("T")


def get_environ_variable(
        name: str,
        default: Optional[str] = None,
        enforce: bool = False,
        apply: Optional[Callable[[Optional[str]], T]] = None,
) -> Optional[Union[Optional[str], T]]:
    return (apply or (lambda x: x))(  # type: ignore
        os.environ.get(name, default=default) if not enforce else
        os.environ.get(name) or (lambda: (_ for _ in ())
                                 .throw(ValueError(f"Missing environ variable: {name}")))()
    )


# Logger configuration
default_logger_configuration = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "standard": {
            "format": get_environ_variable(
                name="DEFAULT_PYTHON_LOGGER",
                default="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
            )
        },
    },
    "handlers": {
        "default": {
            "level": get_environ_variable(
                name="DEFAULT_PYTHON_HANDLER_LEVEL",
                default="INFO"
            ),
            "formatter": "standard",
            "class": "logging.StreamHandler",
        },
    },
    "loggers": {
        "": {
            "handlers": [
                "default"
            ],
            "level": get_environ_variable(
                name="DEFAULT_PYTHON_LOGGER_LEVEL",
                default="INFO",
            ),
            "propagate": True
        }
    }
}


def configure_logger_callable(config_dictionary: Optional[Dict] = None) -> Callable:
    def get_logger(name: str):
        dictConfig(config_dictionary or default_logger_configuration)
        return logging.getLogger(name)
    return get_logger


class LoggerManager:

    def __init__(self, config_dictionary: Optional[Dict] = None):
        self.config_dictionary: Dict = config_dictionary or default_logger_configuration

    def set_configuration(self, **kwargs):
        self.config_dictionary = kwargs

    def get_logger(self, name: str, overwrite_config_dictionary: Optional[Dict] = None):
        dictConfig(overwrite_config_dictionary or self.config_dictionary)
        return logging.getLogger(name)


logger_manager = LoggerManager()
