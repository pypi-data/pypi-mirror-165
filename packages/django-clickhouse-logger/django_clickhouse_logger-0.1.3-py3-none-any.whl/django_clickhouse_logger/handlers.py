import logging
from logging import StreamHandler

from clickhouse_logger.proxy import clickhouse
from django.core.handlers.wsgi import WSGIRequest


class ClickhouseLoggerHandler(StreamHandler):

    def emit(self, record) -> None:
        if isinstance(record, logging.LogRecord) and getattr(record, 'request', False):
            if isinstance(record.request, WSGIRequest):
                clickhouse.proxy(record)
