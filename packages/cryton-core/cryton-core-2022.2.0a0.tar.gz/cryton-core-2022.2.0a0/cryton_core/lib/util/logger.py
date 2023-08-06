import logging.config

import structlog

from cryton_core.etc import config

"""
Default Cryton logger setup and configuration
"""

structlog.configure(
    processors=[
        structlog.stdlib.filter_by_level,
        structlog.stdlib.add_logger_name,
        structlog.stdlib.add_log_level,
        structlog.stdlib.PositionalArgumentsFormatter(),
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.StackInfoRenderer(),
        structlog.processors.format_exc_info,
        structlog.processors.UnicodeDecoder(),
        structlog.processors.JSONRenderer()
    ],
    context_class=dict,
    logger_factory=structlog.stdlib.LoggerFactory(),
    wrapper_class=structlog.stdlib.BoundLogger,
    cache_logger_on_first_use=True,
)

config_dict = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "simple": {  # TODO: remove the trailing `, ` and update 'util.get_logs()' accordingly
            "format": "%(asctime)s.%(msecs)03d %(levelname)s [%(thread)d] {%(module)s} [%(funcName)s] %(message)s, "
        }
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "level": "DEBUG",
            "formatter": "simple",
            "stream": "ext://sys.stdout"
        },
        "debug_logger": {
            "class": "logging.handlers.RotatingFileHandler",
            "level": "DEBUG",
            "formatter": "simple",
            "filename": config.LOG_FILE_PATH_DEBUG,
            "maxBytes": 10485760,
            "backupCount": 20,
            "encoding": "utf8"
        },
        "prod_logger": {
            "class": "logging.handlers.RotatingFileHandler",
            "level": "DEBUG",
            "formatter": "simple",
            "filename": config.LOG_FILE_PATH,
            "maxBytes": 10485760,
            "backupCount": 20,
            "encoding": "utf8"
        }
    },
    "root": {
        "level": "NOTSET",
        "handlers": [],
        "propagate": True
    },
    "loggers": {
        "cryton-core": {
            "level": "INFO",
            "handlers": ["prod_logger"],
            "propagate": True
        },
        "cryton-core-debug": {
            "level": "DEBUG",
            "handlers": ["debug_logger", "console"],
            "propagate": True
        },
        "cryton-core-test": {
            "level": "DEBUG",
            "handlers": ["console"],
            "propagate": False
        }
    }
}

logging.config.dictConfig(config_dict)
# TODO: supress the `amqpstorm` logger

if config.DEBUG:
    logger = structlog.get_logger("cryton-core-debug")
    logger.setLevel(logging.DEBUG)
else:
    logger = structlog.get_logger("cryton-core")
    logger.setLevel(logging.INFO)
