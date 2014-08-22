from __future__ import print_function, unicode_literals

import sys, io
import asyncio
from asyncio import get_event_loop, sleep, coroutine, Future

if sys.version_info >= (3, 4):
    from .transports import async_http as transport
else:
    from .transports import blocking_http as transport

    close  <bound method HTTPConnection.close of <http.client.HTTPConnection object at 0x1026192e8>>
    connect  <bound method HTTPConnection.connect of <http.client.HTTPConnection object at 0x1026192e8>>
    endheaders  <bound method HTTPConnection.endheaders of <http.client.HTTPConnection object at 0x1026192e8>>
    getresponse  <bound method HTTPConnection.getresponse of <http.client.HTTPConnection object at 0x1026192e8>>
    putheader  <bound method HTTPConnection.putheader of <http.client.HTTPConnection object at 0x1026192e8>>
    putrequest  <bound method HTTPConnection.putrequest of <http.client.HTTPConnection object at 0x1026192e8>>
    request  <bound method HTTPConnection.request of <http.client.HTTPConnection object at 0x1026192e8>>
    response_class  <class 'http.client.HTTPResponse'>
    send  <bound method HTTPConnection.send of <http.client.HTTPConnection object at 0x1026192e8>>
    set_debuglevel  <bound method HTTPConnection.set_debuglevel of <http.client.HTTPConnection object at 0x1026192e8>>
    set_tunnel  <bound method HTTPConnection.set_tunnel of <http.client.HTTPConnection object at 0x1026192e8>>

class _HTTPConnectionInterface(object):
    """
    Provides compatibility with the http.client.HTTPConnection API.
    """
    def __init__(self, *args, **kwargs):
        raise NotImplementedError("Use the HTTPConnection class instead.")

    def request(self, method, url, body=None, headers={}):
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

        self._loop.run_until_complete(self._done)
        return self.response

    def getresponse(self):
        pass

    def set_debuglevel(level):
        pass

    def set_tunnel(host, port=None, headers=None):
        pass

    def connect(self):
        self._conn = self._loop.create_connection(lambda: self, self.host, self.port)
        self._loop.run_until_complete(self._conn)

    def close(self):
        pass
        #self._conn.close()

    def putrequest(request, selector, skip_host=False, skip_accept_encoding=False):
        pass

    def putheader(header, argument):
        pass

    def endheaders(message_body=None):
        pass

    def send(data):
        pass

class _ProtocolInterface(asyncio.Protocol):
    """
    Provides compatibility with the http.client.HTTPConnection API.
    """
    def __init__(self, *args, **kwargs):
        raise NotImplementedError("Use the HTTPConnection class instead.")

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

class HTTPConnection(_HTTPConnectionInterface, _ProtocolInterface):
    def __init__(self, host, port=None, timeout=None, source_address=None):
        self.host = host
        self.port = port if port is not None else 80
        self.timeout = timeout
        self.source_address = source_address
        self._loop = get_event_loop()
        self._conn = None

    def __del__(self):
        self.close()

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
            yield from sleep(0)
            yield from self._send_chunk(c)

        self.transport.write(b"0\r\n\r\n")
        print("Done writing body")

    @coroutine
    def _send_chunk(self, chunk):
        self.transport.write(bytes("{:x}\r\n".format(len(chunk)), encoding="utf-8"))
        self.transport.write(chunk)
        self.transport.write(b"\r\n")
        print("Wrote", len(chunk), "bytes")

class HTTPSConnection(HTTPConnection):
    def __init__(self, host, port=None, timeout=None, source_address=None, context=None, check_hostname=None):
        pass

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
