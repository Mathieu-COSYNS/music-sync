import logging
import logging.config

LOG_LEVELS = {
    'D': 'DEBUG',
    'I': 'INFO',
    'W': 'WARNING',
    'E': 'ERROR',
    'C': 'CRITICAL',
}


class TerminalFormatter(logging.Formatter):

    grey = "\x1b[38;20m"
    yellow = "\x1b[33;20m"
    red = "\x1b[31;20m"
    bold_red = "\x1b[31;1m"
    reset = "\x1b[0m"
    format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s (%(filename)s:%(lineno)d)"

    FORMATS = {
        logging.DEBUG: grey + format + reset,
        logging.INFO: grey + format + reset,
        logging.WARNING: yellow + format + reset,
        logging.ERROR: red + format + reset,
        logging.CRITICAL: bold_red + format + reset
    }

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)


def setup_logging(level: str | None = None):
    level_clean = level.upper()
    level_clean = LOG_LEVELS.get(level_clean, level_clean)

    if not isinstance(getattr(logging, level_clean, None), int):
        raise ValueError('Invalid log level: %s' % level)

    logging_config = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "terminal": {
                "class": "colorlog.ColoredFormatter",
                "format": "%(log_color)s%(levelname)-8s%(reset)s | %(log_color)s%(message)s%(reset)s",
            },
            "precise": {
                "format": "%(asctime)s [%(levelname)s][%(name)s]: %(message)s",
                "datefmt": "%Y-%m-%dT%H:%M:%S%z",
            }
        },
        "handlers": {
            "stdout": {
                "class": "logging.StreamHandler",
                "formatter": "terminal",
                "stream": "ext://sys.stdout",
            },
            "file": {
                "class": "logging.handlers.RotatingFileHandler",
                "formatter": "precise",
                "filename": "music_sync.log",
                "maxBytes": 1024 * 1024,  # <1MB
                "backupCount": 3
            }
        },
        "loggers": {"": {"handlers": ["stdout", "file"], "level": level_clean}},
    }

    logging.config.dictConfig(logging_config)
