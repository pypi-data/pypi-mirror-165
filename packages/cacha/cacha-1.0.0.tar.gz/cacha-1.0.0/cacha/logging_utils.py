"""Logging configuration."""
import logging.config


# Logging format example:
# 2018/11/20 12:36:37 INFO cacha.cache: Message
LOGGING_LINE_FORMAT = "%(asctime)s %(levelname)s %(name)s: %(message)s"
LOGGING_DATETIME_FORMAT = "%Y/%m/%d %H:%M:%S"


def configure_loggers(root_module_name):
    """Configure package loggers."""
    logging.config.dictConfig(
        {
            "version": 1,
            "disable_existing_loggers": False,
            "formatters": {
                "standard": {
                    "format": LOGGING_LINE_FORMAT,
                    "datefmt": LOGGING_DATETIME_FORMAT,
                },
            },
            "handlers": {
                "default": {
                    "formatter": "standard",
                    "class": "logging.StreamHandler",
                    "stream": "ext://sys.stdout",
                },
            },
            "loggers": {
                root_module_name: {
                    "handlers": ["default"],
                    "level": "INFO",
                    "propagate": False,
                },
            },
        }
    )
