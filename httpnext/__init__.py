from __future__ import print_function, unicode_literals

import sys, io, socket

HTTP_PORT = 80
HTTPS_PORT = 443

if sys.version_info >= (3, 4):
    from .transports import async_http as transport
else:
    from .transports import blocking_http as transport

class HTTPResponse(io.RawIOBase):
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

class _HTTPConnectionInterface(object):
    """
    Provides compatibility with the http.client.HTTPConnection API.
    """
    response_class = HTTPResponse
    default_port = HTTP_PORT
    auto_open = 1
    debuglevel = 0
    # TCP Maximum Segment Size (MSS) is determined by the TCP stack on
    # a per-connection basis.  There is no simple and efficient
    # platform independent mechanism for determining the MSS, so
    # instead a reasonable estimate is chosen.  The getsockopt()
    # interface using the TCP_MAXSEG parameter may be a suitable
    # approach on some operating systems. A value of 16KiB is chosen
    # as a reasonable estimate of the maximum MSS.
    mss = 16384

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

class HTTPConnection(_HTTPConnectionInterface, transport._ProtocolInterface):
    def __init__(self, host, port=None, timeout=socket._GLOBAL_DEFAULT_TIMEOUT, source_address=None):
        # The following 5 fields are part of the http.client.HTTPConnection interface.
        self.host = host
        self.port = port if port is not None else HTTP_PORT
        self.source_address = source_address
        self.sock = None
        self.timeout = timeout

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

    def on(self, event):
        pass

class HTTPSConnection(HTTPConnection):
    def __init__(self, host, port=None, timeout=None, source_address=None, context=None, check_hostname=None):
        pass
