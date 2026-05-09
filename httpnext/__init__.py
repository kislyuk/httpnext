from __future__ import absolute_import, division, print_function, unicode_literals

import sys, io, socket, time
import http.client

HTTP_PORT = 80
HTTPS_PORT = 443

class HTTPResponse(io.BufferedIOBase):
    def __init__(self, debuglevel=0):
        self.debuglevel = debuglevel
        self.headers = self.msg = None

        self.version = http.client._UNKNOWN
        self.status = http.client._UNKNOWN
        self.reason = http.client._UNKNOWN

        self.chunked = http.client._UNKNOWN
        self.chunk_left = http.client._UNKNOWN
        self.length = http.client._UNKNOWN
        self.will_close = http.client._UNKNOWN

    def read(self, amt=None):
        pass

    def readinto(self, b):
        pass

    def getheader(self, name, default=None):
        pass

    def getheaders(self):
        pass

    def fileno(self):
        pass

    def __iter__(self):
        # Chunked response iterator
        pass

    def __enter__(self):
        pass

    def __exit__(self):
        pass

    def on(self, event):
        pass

import asyncio

class HTTPConnection(asyncio.Protocol):
    response_class = HTTPResponse
    default_port = HTTP_PORT
    auto_open = 1
    debuglevel = 0

    # Not used.
    mss = 16384

    def __init__(self, host, port=None, timeout=socket._GLOBAL_DEFAULT_TIMEOUT, source_address=None):
        self.host = host
        self.port = port if port is not None else HTTP_PORT
        self.source_address = source_address
        self.sock = None
        self.timeout = timeout

        self._transport = None
#        self._event_loop = asyncio.get_event_loop()

    def connection_made(self, transport):
        peername = transport.get_extra_info('peername')
        print('Connection established to', peername, transport)
        self._transport = transport

    def request(self, method, url, body=None, headers=None):
        self._method = method
        self._url = url
        if headers is None:
            headers = {}
#        headers["Transfer-Encoding"] = "chunked"
        self._headers = headers
        self._body = body
        self._response = HTTPResponse()
        self._request_future = asyncio.async(self._send_request())

        try:
            asyncio.get_event_loop().run_until_complete(self._request_future)
        except asyncio.CancelledError:
            print("Got cancellation")

    @asyncio.coroutine
    def _send_request(self):
        yield from self._connect()
        yield from self._send_head()
        yield from asyncio.sleep(2)
        yield from self._send_body()
        print("Done sending request")

    @asyncio.coroutine
    def _send_head(self):
        self._transport.write("{} {} HTTP/1.1\r\n".format(self._method, self._url).encode())
        for header in self._headers:
            self._transport.write("{}:{}\r\n".format(header, self._headers[header]).encode())
        self._transport.write(b"\r\n")
        print("Sent head")

        """
        if method == "POST":
            headers["Expect"] = "100-continue"
#            headers["Content-Length"] = str(len(body))
            headers["Transfer-Encoding"] = "chunked"
        self._ready_to_send_body = False
        self._eof_received = False
        self.body = body
        self.response = b""
        self.transport.write("{} {} HTTP/1.1\r\n".format(method, url).encode())
        for header in headers:
            self.transport.write("{}:{}\r\n".format(header, headers[header]).encode())
        self.transport.write(b"\r\n")
        self._send_body()
        return self.response
        """

    @asyncio.coroutine
    def _send_body(self):
        if self._body is not None:
            self._transport.write(self._body)
            print("Sent body")

    def data_received(self, data):
        print("Received:", data)

    def connection_lost(self, exc):
        print("Connection lost")
        self._request_future.cancel()
        asyncio.get_event_loop().stop()

    def getresponse(self):
        print("In getresponse")
        asyncio.get_event_loop().run_forever()
        
        return None

    def set_debuglevel(level):
        pass

    def set_tunnel(host, port=None, headers=None):
        pass

    def connect(self):
        return
        if self._transport is None:
            asyncio.get_event_loop().run_until_complete(self._connect())

    @asyncio.coroutine
    def _connect(self):
        self._transport, protocol = yield from asyncio.get_event_loop().create_connection(lambda: self, self.host, self.port)

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

"""
class HTTPConnection(_HTTPConnectionInterface, transport._ProtocolInterface):
    def __del__(self):
        self.close()

    # Is this needed here, or only in HTTPResponse?
    def on(self, event):
        pass

class HTTPSConnection(HTTPConnection):
    def __init__(self, host, port=None, timeout=None, source_address=None, context=None, check_hostname=None):
        pass
CS169
"""
