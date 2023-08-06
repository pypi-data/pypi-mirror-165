# -*- coding: utf-8 -*-

__author__ = r'wsb310@gmail.com'

import os
import sys
import time
import signal

from typing import Callable

from multiprocessing import Process
from multiprocessing.shared_memory import SharedMemory

from .base import Utils
from .interface import ContextManager, RunnableInterface
from .struct import ByteArrayAbstract


def fork_processes() -> int:

    pid = os.fork()

    if pid == 0:
        Utils.urandom_seed()

    return pid


class Daemon(RunnableInterface):

    def __init__(
            self, target: Callable, sub_process_num: int, *,
            keep_live: bool = False, join_timeout: int = 10, **kwargs
    ):

        self._target = target
        self._kwargs = kwargs

        self._sub_process = set()
        self._sub_process_num = sub_process_num

        self._keep_live = keep_live
        self._join_timeout = join_timeout

        signal.signal(signal.SIGINT, self._kill_process)
        signal.signal(signal.SIGTERM, self._kill_process)

    def _kill_process(self, *_):

        self._keep_live = False

        for process in self._sub_process:
            os.kill(process.ident, signal.SIGINT)

        for process in self._sub_process:
            process.join(self._join_timeout)
            process.kill()

        sys.exit()

    def _fill_process(self):

        while len(self._sub_process) < self._sub_process_num:

            process = Process(target=self._target, kwargs=self._kwargs)
            process.start()

            self._sub_process.add(process)

    def _check_process(self):

        for process in self._sub_process.copy():

            if not process.is_alive():
                self._sub_process.remove(process)

        if self._keep_live is True:
            self._fill_process()

    def is_active(self):

        return self._keep_live or (len(self._sub_process) > 0)

    def run(self):

        self._fill_process()

        while self.is_active():
            self._check_process()
            time.sleep(0.1)


class SharedByteArray(ByteArrayAbstract, ContextManager):

    def __init__(self, name=None, create=False, size=0):

        ByteArrayAbstract.__init__(self)

        self._shared_memory = SharedMemory(name, create, size)
        self._create_mode = create

    def _context_release(self):

        self.release()

    def release(self):

        self._shared_memory.close()

        if self._create_mode:
            self._shared_memory.unlink()

    def read(self, size):

        return self._shared_memory.buf[:size]

    def write(self, buffer):

        self._shared_memory.buf[:len(buffer)] = buffer


class HeartbeatChecker(ContextManager):

    def __init__(self, name=r'default', timeout=60):

        self._name = f'heartbeat_{name}'

        self._timeout = timeout

        try:
            self._byte_array = SharedByteArray(self._name, True, 8)
        except Exception as _:
            self._byte_array = SharedByteArray(self._name)

    def _context_release(self):

        self.release()

    @property
    def refresh_time(self):

        if self._byte_array is not None:
            return self._byte_array.read_unsigned_int()
        else:
            return 0

    def release(self):

        if self._byte_array is not None:
            self._byte_array.release()
            self._byte_array = None

    def check(self):

        return (Utils.timestamp() - self.refresh_time) < self._timeout

    def refresh(self):

        if self._byte_array is not None:
            self._byte_array.write_unsigned_int(Utils.timestamp())
