# -*- coding: utf-8 -*-

__author__ = r'wsb310@gmail.com'

import inspect
import aio_pika

from typing import Dict, Callable

from .publish import RabbitMQProducerForExchangePool
from .consume import RabbitMQConsumerForExchange

from ...extend.error import catch_error
from ...extend.asyncio.base import Utils, FutureWithTimeout


class RpcServer:

    def __init__(
            self, url: str, pool_size: int, exchange_name: str, *,
            server_name: str = None, response_timeout: int = 60
    ):

        self._rpc_function: Dict[str, Callable] = {}

        self._producer = RabbitMQProducerForExchangePool(
            url, pool_size, exchange_name,
            exchange_type=aio_pika.ExchangeType.DIRECT
        )

        self._consumer = RabbitMQConsumerForExchange(url)
        self._consumer.config(
            exchange_name, self._consume_message, True,
            queue_config={
                r'name': f'rpc_server:{server_name}' if server_name is not None else r'rpc_server',
                r'arguments': {r'x-message-ttl': int(response_timeout * 1000)}
            }
        )

    async def initialize(self):

        self._rpc_function[r'ping'] = lambda: r'pong'

        await self._producer.connect()
        await self._consumer.connect()

    async def release(self):

        await self._producer.close()
        await self._consumer.close()

        self._rpc_function.clear()

    async def _consume_message(self, message: aio_pika.Message):

        with catch_error():

            _message = Utils.msgpack_decode(message.body)

            Utils.log.info(f'rpc client request: {_message}')

            _func_name = _message.get(r'name')
            _func_args = _message.get(r'args')
            _func_kwargs = _message.get(r'kwargs')

            if _func_name in self._rpc_function:

                try:

                    result = self._rpc_function[_func_name](*_func_args, **_func_kwargs)

                    if inspect.isawaitable(result):
                        result = await result

                    response = {
                        r'name': _func_name,
                        r'data': result,
                    }

                except Exception as err:

                    response = {
                        r'name': _func_name,
                        r'error': str(err),
                    }

            else:

                response = {
                    r'name': _func_name,
                    r'error': r'function not found',
                }

            await self._producer.publish(
                aio_pika.Message(
                    body=Utils.msgpack_encode(response),
                    correlation_id=message.correlation_id
                ),
                routing_key=message.reply_to
            )

    def register(self, name: str, func: Callable):

        self._rpc_function[name] = func

        Utils.log.info(f'rpc server register {name} {func}')


class RpcClient:

    def __init__(
            self, url: str, pool_size: int, exchange_name: str, *,
            request_timeout: int = 60
    ):

        self._futures: Dict[str, FutureWithTimeout] = {}
        self._request_timeout = request_timeout

        self._producer = RabbitMQProducerForExchangePool(
            url, pool_size, exchange_name,
            exchange_type=aio_pika.ExchangeType.DIRECT
        )

        self._consumer = RabbitMQConsumerForExchange(url)
        self._consumer.config(
            exchange_name, self._consume_message, True,
            queue_config={
                r'name': f'rpc_client:{Utils.uuid1()}',
                r'exclusive': True,
                r'arguments': {r'x-message-ttl': int(request_timeout * 1000)}
            }
        )

    async def initialize(self):

        await self._producer.connect()
        await self._consumer.connect()

    async def release(self):

        await self._producer.close()
        await self._consumer.close()

    def _consume_message(self, message: aio_pika.Message):

        with catch_error():

            response = Utils.msgpack_decode(message.body)

            if message.correlation_id in self._futures:

                self._futures.get(
                    message.correlation_id
                ).set_result(
                    response
                )

    async def call(self, name: str, *, args=None, kwargs=None, server_name: str = None):

        result = None

        correlation_id = Utils.uuid1()

        future = self._futures[correlation_id] = FutureWithTimeout(self._request_timeout)

        try:

            await self._producer.publish(
                aio_pika.Message(
                    Utils.msgpack_encode(
                        {
                            r'name': name,
                            r'args': args if args is not None else [],
                            r'kwargs': kwargs if kwargs is not None else {},
                        }
                    ),
                    correlation_id=correlation_id,
                    reply_to=self._consumer.queue_name,
                ),
                routing_key=f'rpc_server:{server_name}' if server_name is not None else r'rpc_server',
            )

            result = await future

        except Exception as err:

            Utils.log.error(str(err))

        finally:

            del self._futures[correlation_id]

        if not result:
            raise Exception(r'rpc call error')

        if r'error' in result:
            raise Exception(result[r'error'])

        return result[r'data']
