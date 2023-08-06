# -*- coding: utf-8 -*-

__author__ = r'wsb310@gmail.com'

import os
import sys
import queue
import logging

from threading import Thread
from datetime import timedelta

from loguru._file_sink import FileSink

from elasticsearch import Elasticsearch, helpers as es_helpers

from .trace import get_trace_id
from .base import Utils


class LogFileRotator:

    @classmethod
    def make(cls, _size=500, _time=r'00:00'):

        return cls(_size, _time).should_rotate

    def __init__(self, _size, _time):

        _size = _size * (1024 ** 2)
        _time = Utils.split_int(_time, r':')

        now_time = Utils.today()

        self._size_limit = _size
        self._time_limit = now_time.replace(hour=_time[0], minute=_time[1])

        if now_time >= self._time_limit:
            self._time_limit += timedelta(days=1)

    def should_rotate(self, message, file):

        file.seek(0, 2)

        if file.tell() + len(message) > self._size_limit:
            return True

        if message.record[r'time'].timestamp() > self._time_limit.timestamp():
            self._time_limit += timedelta(days=1)
            return True

        return False


DEFAULT_LOG_FILE_ROTATOR = LogFileRotator.make()


class InterceptHandler(logging.Handler):
    """日志拦截器
    """

    def emit(self, record):

        Utils.log.opt(
            depth=8,
            exception=record.exc_info
        ).log(
            record.levelname,
            record.getMessage()
        )


class ElasticsearchDataStreamUtil:

    def __init__(
            self, elasticsearch: Elasticsearch, alias_name: str, *,
            rollover_max_age: str = r'1d', rollover_max_primary_shard_size: str = r'50gb',
            delete_min_age: str = r'30d', refresh_interval: str = r'5s', timestamp_order: str = r'desc'
    ):

        self._elasticsearch = elasticsearch

        self._alias_name = alias_name
        self._policy_name = f'{alias_name}-ilm-policy'

        self._rollover_max_age = rollover_max_age
        self._rollover_max_primary_shard_size = rollover_max_primary_shard_size

        self._delete_min_age = delete_min_age
        self._refresh_interval = refresh_interval
        self._timestamp_order = timestamp_order

    def initialize(self):

        try:

            indices = self._elasticsearch.indices

            if not indices.exists_alias(name=self._alias_name):
                self._create_lifecycle()
                self._create_index_template()

        except Exception as err:

            sys.stderr.write(str(err))

    def _create_lifecycle(self):

        policy = {
            r'phases': {
                r'hot': {
                    r'actions': {
                        r'rollover': {
                            r'max_age': self._rollover_max_age,
                            r'max_primary_shard_size': self._rollover_max_primary_shard_size,
                        },
                        r'set_priority': {
                            r'priority': 100,
                        }
                    },
                    r'min_age': r'0ms',
                },
                r'delete': {
                    r'actions': {
                        r'delete': {}
                    },
                    r'min_age': self._delete_min_age,
                },
            },
        }

        self._elasticsearch.ilm.put_lifecycle(name=self._policy_name, policy=policy)

    def _create_index_template(self):

        mappings = {
            r'dynamic': r'strict',
            r'properties': {
                r'extra': {
                    r'type': r'flattened',
                },
                r'process': {
                    r'properties': {
                        r'id': {
                            r'type': r'keyword',
                        },
                        r'name': {
                            r'type': r'keyword',
                            r'ignore_above': 64,
                        },
                    },
                },
                r'thread': {
                    r'properties': {
                        r'id': {
                            r'type': r'keyword',
                        },
                        r'name': {
                            r'type': r'keyword',
                            r'ignore_above': 64,
                        },
                    },
                },
                r'level': {
                    r'properties': {
                        r'no': {
                            r'type': r'integer',
                        },
                        r'name': {
                            r'type': r'keyword',
                            r'ignore_above': 64,
                        },
                    },
                },
                r'module': {
                    r'type': r'text',
                },
                r'message': {
                    r'type': r'text',
                    r'analyzer': r'ik_max_word',
                    r'search_analyzer': r'ik_smart',
                },
                r'@timestamp': {
                    r'type': r'date',
                    r'format': r'epoch_millis',
                },
            }
        }

        template = {
            r'settings': {
                r'index': {
                    r'lifecycle': {
                        r'name': self._policy_name,
                    },
                    r'refresh_interval': self._refresh_interval,
                    r'sort': {
                        r'field': r'@timestamp',
                        r'order': self._timestamp_order,
                    }
                },
            },
            r'mappings': mappings,
        }

        self._elasticsearch.indices.put_index_template(
            name=self._alias_name,
            template=template,
            index_patterns=[f'{self._alias_name}*'],
            data_stream={},
        )


class ElasticsearchSink:
    """Elasticsearch日志投递
    """

    def __init__(
            self, hosts, index, *,
            buffer_maxsize=0xffff,
            rollover_max_age: str = r'1d', rollover_max_primary_shard_size: str = r'50gb',
            delete_min_age: str = r'30d',
            **kwargs):

        self._elasticsearch = Elasticsearch(hosts, **kwargs)

        self._index = index

        self._buffer = queue.Queue(buffer_maxsize)
        self._closed = False

        self._task = Thread(target=self._do_task)
        self._task.start()

        ElasticsearchDataStreamUtil(
            self._elasticsearch, index,
            rollover_max_age=rollover_max_age, rollover_max_primary_shard_size=rollover_max_primary_shard_size,
            delete_min_age=delete_min_age
        ).initialize()

    def write(self, message):

        log_extra = message.record[r'extra']

        if r'trace_id' not in log_extra and (trace_id := get_trace_id()) is not None:
            log_extra[r'trace_id'] = trace_id

        try:
            self._buffer.put(message, block=True, timeout=1)
        except queue.Full as _:
            if message.record[r'level'].no > logging.INFO:
                sys.stderr.write(str(message))

    def close(self):

        self._closed = True
        self._task.join(10)

    def _do_task(self):

        current_ident = self._task.ident

        while not self._closed:

            try:

                records = [self._buffer.get(block=True, timeout=1).record]

                for _ in range(min(self._buffer.qsize(), 1000)):
                    records.append(self._buffer.get_nowait().record)

                if records:
                    es_helpers.bulk(
                        self._elasticsearch,
                        actions=[
                            {
                                r'_op_type': r'create',
                                r'_index': self._index,
                                r'extra': _row[r'extra'],
                                r'process': {
                                    r'id': _row[r'process'].id,
                                    r'name': _row[r'process'].name,
                                },
                                r'thread': {
                                    r'id': _row[r'thread'].id,
                                    r'name': _row[r'thread'].name,
                                },
                                r'level': {
                                    r'no': _row[r'level'].no,
                                    r'name': _row[r'level'].name,
                                },
                                r'module': f"{_row[r'name']}:{_row[r'function']}:{_row[r'line']}",
                                r'message': _row[r'message'],
                                r'@timestamp': int(_row[r'time'].timestamp() * 1000),
                            }
                            for _row in records if current_ident != _row[r'thread'].id
                        ]
                    )

            except queue.Empty as _:

                pass

            except Exception as err:

                sys.stderr.write(str(err))


class QueuedFileSink(FileSink):
    """日志文件队列
    """

    def __init__(self, path, *, buffer_maxsize=0xffff, **kwargs):

        super().__init__(path, **kwargs)

        self._buffer = queue.Queue(buffer_maxsize)

        self._worker = Thread(target=self._queued_writer)
        self._running = True

        self._worker.start()

    def write(self, message):

        try:
            self._buffer.put(message, block=True, timeout=1)
        except queue.Full as _:
            if message.record[r'level'].no > logging.INFO:
                sys.stderr.write(str(message))

    def stop(self):

        self._running = False
        self._worker.join(10)

        super().stop()

    def _queued_writer(self):

        while self._running:

            try:
                super().write(
                    self._buffer.get(block=True, timeout=10)
                )
            except queue.Empty as _:
                pass
            except Exception as err:
                sys.stderr.write(str(err))


DEFAULT_LOG_FILE_NAME = r'runtime_{time}.log'


def init_logger(
        level, *, handler=None,
        file_path=None, file_name=DEFAULT_LOG_FILE_NAME,
        file_rotation=DEFAULT_LOG_FILE_ROTATOR, file_retention=0xff,
        extra=None, enqueue=False, debug=False
):

    level = level.upper()

    Utils.log.remove()

    if extra is not None and (extra := {_key: _val for _key, _val in extra.items() if _val is not None}):
        Utils.log.configure(extra=extra)

    if handler or file_path:

        if handler:
            Utils.log.add(
                handler,
                level=level,
                enqueue=enqueue,
                backtrace=debug
            )

        if file_path:

            _file_name, _file_ext_name = os.path.splitext(file_name)

            Utils.log.add(
                QueuedFileSink(
                    Utils.path.join(file_path, _file_name + '.pid-' + str(Utils.getpid()) + _file_ext_name),
                    rotation=file_rotation,
                    retention=file_retention
                ),
                level=level,
                enqueue=enqueue,
                backtrace=debug
            )

    else:

        Utils.log.add(
            sys.stderr,
            level=level,
            enqueue=enqueue,
            backtrace=debug
        )

    logger = logging.getLogger()
    logger.setLevel(level)
    logger.addHandler(InterceptHandler())
