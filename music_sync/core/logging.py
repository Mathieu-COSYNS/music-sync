import logging
import logging.config

LOG_LEVELS = {
    "D": "DEBUG",
    "I": "INFO",
    "W": "WARNING",
    "E": "ERROR",
    "C": "CRITICAL",
}


def setup_logging(level: str | None = None):
    level_clean = level.upper() if level is not None else "I"
    level_clean = LOG_LEVELS.get(level_clean, "INFO")

    if not isinstance(getattr(logging, level_clean, None), int):
        raise ValueError(f"Invalid log level: {level}")

    logging_config = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "terminal": {
                "class": "colorlog.ColoredFormatter",
                "format": "%(log_color)s%(levelname)-8s%(reset)s |"
                + " %(log_color)s%(message)s%(reset)s",
            },
            "precise": {
                "format": "%(asctime)s [%(levelname)s][%(name)s]: %(message)s",
                "datefmt": "%Y-%m-%dT%H:%M:%S%z",
            },
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
                "backupCount": 3,
            },
        },
        "loggers": {"": {"handlers": ["stdout", "file"], "level": level_clean}},
    }

    logging.config.dictConfig(logging_config)
