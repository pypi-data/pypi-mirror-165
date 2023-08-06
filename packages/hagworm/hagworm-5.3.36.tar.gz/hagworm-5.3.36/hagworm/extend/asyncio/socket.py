# -*- coding: utf-8 -*-

__author__ = r'wsb310@gmail.com'

import signal
import socket
import asyncio

from hagworm import hagworm_slogan
from hagworm import __version__ as hagworm_version
from hagworm.extend.asyncio.base import Utils, install_uvloop
from hagworm.extend.interface import RunnableInterface

from ..error import RouterError


class Router:

    def __init__(self, root=r''):

        self._root = root
        self._reg_func = {}

    def __repr__(self):

        return self._reg_func.__repr__()

    async def __call__(self, method, *args, **kwargs):

        func = self._reg_func.get(method)

        if not func:
            raise RouterError(f'{method} not exists')

        return await func(*args, **kwargs)

    def _reg(self, method, func):

        _method = f'{self._root}{method}'

        if _method in self._reg_func:
            raise RouterError(f'{method} has exists')

        self._reg_func[_method] = func

    def reg(self, method):

        def _reg_func(func):
            self._reg(method, func)
            return func

        return _reg_func

    def items(self):

        return self._reg_func.items()

    def include(self, router):

        for method, func in router.items():
            self._reg(method, func)


class AsyncTcpServer(RunnableInterface):

    def __init__(
            self, client_connected_cb, address, *,
            backlog=None, buffer_limit=0xA0000,
            on_startup=None, on_shutdown=None
    ):

        self._client_connected_cb = client_connected_cb

        self._address = address
        self._backlog = backlog
        self._buffer_limit = buffer_limit

        self._on_startup = on_startup
        self._on_shutdown = on_shutdown

        self._server = None
        self._server_task = None

        signal.signal(signal.SIGINT, self._exit)
        signal.signal(signal.SIGTERM, self._exit)

    def run(self):

        environment = Utils.environment()

        Utils.log.info(
            f'{hagworm_slogan}'
            f'hagworm {hagworm_version}\n'
            f'python {environment["python"]}\n'
            f'system {" ".join(environment["system"])}'
        )

        install_uvloop()

        asyncio.run(self._run())

    async def _run(self):

        sock = socket.create_server(self._address, family=socket.AF_INET, backlog=self._backlog, reuse_port=True)

        if self._on_startup is not None:
            await self._on_startup()

        Utils.log.success(f'tcp server [pid:{Utils.getpid()}] startup complete: {sock.getsockname()}')

        self._server = await asyncio.start_server(self._client_connected_cb, limit=self._buffer_limit, sock=sock)

        async with self._server:

            self._server_task = asyncio.create_task(self._server.serve_forever())

            try:
                await self._server_task
            except asyncio.CancelledError as _:
                pass

        if self._on_shutdown is not None:
            await self._on_shutdown()

        Utils.log.success(f'tcp server [pid:{Utils.getpid()}] shutdown')

    def _exit(self, *_):

        if self._server_task is not None:
            self._server_task.cancel()
