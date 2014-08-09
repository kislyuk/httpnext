from __future__ import print_function, unicode_literals

from asyncio import get_event_loop, Protocol, sleep, coroutine

# Should this inherit from both asyncio.protocol and HTTPConnection? (Probably not, but might be OK)

class HTTPConnection(Protocol):
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self._loop = get_event_loop()
        self._conn = None

    def connect(self):
        self._conn = self._loop.create_connection(lambda: self, self.host, self.port)
        self._loop.run_until_complete(self._conn)

    def close(self):
        pass
        #self._conn.close()

    @coroutine
    def driver(self):
        while not self._eof_received:
            print("Waiting...")
            yield from sleep(1)
        print("Done")

    def request(self, method, url, body=None, headers={}):
        self._eof_received = False
        self.response = b""
        self.transport.write("{} {}\n\n".format(method, url).encode())

        self._loop.run_until_complete(self.driver())
        return self.response

    def getresponse(self):
        pass

    def __del__(self):
        self.close()

    def connection_made(self, transport):
        self.transport = transport
        print("Connection made:", transport)

    def connection_lost(self, exc):
        print('server closed the connection')
        #asyncio.get_event_loop().stop()

    def eof_received(self):
        print("Received EOF")
        self._eof_received = True

    def pause_writing(self):
        print("Received pause writing cb")

    def resume_writing(self):
        print("Received resume writing cb")

    def data_received(self, data):
        print("Received data:", data)
        self.response += data

c = HTTPConnection("localhost", 9000)
c.connect()
response = c.request("GET", "/")
print("Got response:", response)

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
