from __future__ import print_function, unicode_literals

from asyncio import get_event_loop, Protocol, sleep, coroutine, Future

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

#    @coroutine
#    def driver(self):
#        while not self._eof_received:
#            print("Waiting...")
#            yield from sleep(1)
#        print("Done")

    def request(self, method, url, body=None, headers={}, callback=None):
        if method == "POST":
            headers["Expect"] = "100-continue"
#            headers["Content-Length"] = str(len(body))
            headers["Transfer-Encoding"] = "chunked"
        self._ready_to_send_body, self._eof_received = False, False
        self.body = body
        self.response = b""
        self.transport.write("{} {} HTTP/1.1\r\n".format(method, url).encode())
        for header in headers:
            self.transport.write("{}:{}\r\n".format(header, headers[header]).encode())
        self.transport.write(b"\r\n")
        self._ready_to_send_body = Future()
        self._loop.run_until_complete(self._ready_to_send_body)
        self._loop.run_until_complete(self._send_body())
        self._done = Future()
        if callback is None:
            self._loop.run_until_complete(self._done)
            return self.response
        else:
            pass

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
        self._done.set_result(None)
#        self._eof_received = True

    def pause_writing(self):
        print("Received pause writing cb")

    def resume_writing(self):
        print("Received resume writing cb")

    def data_received(self, data):
        print("Received data:", data)
        # TODO: fix this up to not be stupid
        if data.startswith(b"HTTP/1.1 100 Continue"):
            print("Got 100 continue, ready to send body")
            self._ready_to_send_body.set_result(None)
        self.response += data

    @coroutine
    def _send_body(self):
        print("Will send body")
        from io import BytesIO
        b = BytesIO(self.body)
        cs = 1024
        while True:
            c = b.read(cs)
            if c == b"":
                break
            yield from sleep(0.1)
            yield from self._send_chunk(c)

        self.transport.write(b"0\r\n\r\n")
        print("Done writing body")

    @coroutine
    def _send_chunk(self, chunk):
        self.transport.write(bytes("{:x}\r\n".format(len(chunk)), encoding="utf-8"))
        self.transport.write(chunk)
        self.transport.write(b"\r\n")
        print("Wrote", len(chunk), "bytes")

c = HTTPConnection("localhost", 9000)
c.connect()
response = c.request("POST", "/", headers={"foo": "bar", "wat": "wat"}, body=b"0123456789ABCDEF"*1024)
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
