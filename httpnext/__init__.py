from __future__ import print_function, unicode_literals

from asyncio import get_event_loop

# Should this inherit from both asyncio.protocol and HTTPConnection? (Probably not, but might be OK)

class HTTPConnection(object):
    def __init__(self, host, port):
        self._loop = get_event_loop()
        self._conn = self._loop.create_connection(FACTORY, host, port)

    def connect(self):
        pass

    def close(self):
        pass

    def request(method, url, body=None, headers={}):
        pass

    def getresponse(self):
        pass

    def __del__(self):
        self.close()

class HTTPResponse(object):
    def __iter__(self):
        # Chunked response iterator
        pass

    def __enter__(self):
        pass
    def __exit__(self):
        pass

    def read(self, amt=None):
        pass
    def readinto(self, b):
        pass
