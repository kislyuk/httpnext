#!/usr/bin/env python3.4

import asyncio, requests
from random import random

class WatClient(asyncio.Protocol):
    def __init__(self, method, resource):
        self.method = method
        self.resource = resource

    def __call__(self):
        return self

    def connection_made(self, transport):
        transport.write("{} {}\n\n".format(self.method, self.resource).encode())
#        print('data sent: {}'.format(self.message))

    def data_received(self, data):
        print('data received: {}'.format(data.decode()))

    def connection_lost(self, exc):
        print('server closed the connection')
#        asyncio.get_event_loop().stop()


@asyncio.coroutine
def h():
    return requests.get("https://google.com")

@asyncio.coroutine
def g(i):
    print("Begin", i)
    result = yield from h()
    print("End", i, result)

@asyncio.coroutine
def f():
    for i in range(10):
        yield from g(i)

loop = asyncio.get_event_loop()
coro = loop.create_connection(WatClient('GET', '/'), 'localhost', 9000)
loop.run_until_complete(coro)
loop.run_forever()
loop.close()
