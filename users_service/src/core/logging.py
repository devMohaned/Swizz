import sys
from enum import Enum

from config.settings import settings
from middleware.request_context import get_request_id
from pythonjsonlogger import json

import logging


class LogFormat(str, Enum):
    TEXT = "text"
    JSON = "json"


class RequestIdFilter(logging.Filter):
    def filter(self, record: logging.LogRecord) -> bool:
        record.requestId = get_request_id() or "-"
        return True


def configure_logging():
    log_format = LogFormat.JSON if settings.log_format.lower() == "json" else LogFormat.TEXT
    level = getattr(logging, settings.log_level.upper(), logging.INFO)

    logger = logging.getLogger()
    logger.setLevel(level)
    logger.handlers.clear()

    request_id_filter = RequestIdFilter()
    # stdout handler
    stream_handler = logging.StreamHandler(sys.stdout)
    stream_handler.addFilter(request_id_filter)

    # file handler
    file_handler = logging.FileHandler(settings.log_file_path)
    file_handler.addFilter(request_id_filter)

    if log_format == LogFormat.JSON:
        formatter = json.JsonFormatter(
            fmt="%(asctime)s %(levelname)s %(name)s %(message)s %(requestId)s",
            rename_fields={
                "asctime": "timestamp",
                "levelname": "level",
                "name": "logger",
                "message": "message",
                "requestId": "requestId",
            },
        )
    else:
        formatter = logging.Formatter(
            fmt="%(asctime)s | %(requestId)s | %(levelname)s | %(name)s | %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )

    stream_handler.setFormatter(formatter)
    file_handler.setFormatter(formatter)

    logger.addHandler(stream_handler)
    logger.addHandler(file_handler)

    logging.info(f"Logging initialized ({log_format.value.upper()} mode, level={settings.log_level.upper()})")


def get_logger(name: str) -> logging.Logger:
    return logging.getLogger(name)
