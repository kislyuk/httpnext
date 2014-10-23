from __future__ import print_function, unicode_literals

import sys, io, socket

HTTP_PORT = 80
HTTPS_PORT = 443

if sys.version_info >= (3, 4):
    from .transports import async_http as transport
else:
    from .transports import blocking_http as transport

class HTTPResponse(io.RawIOBase):
    def __init__(self):
        # msg is a http.client.HTTPMessage
        self.msg = None
        self.version = None
        self.status = None
        self.reason = None
        self.debuglevel = None
        self.closed = False

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

class _HTTPConnectionInterface(object):
    """
    Provides compatibility with the http.client.HTTPConnection API.
    """
    response_class = HTTPResponse
    default_port = HTTP_PORT
    auto_open = 1
    debuglevel = 0

    # Not used.
    mss = 16384

    def __init__(self, host, port, timeout, source_address):
        self.host = host
        self.port = port if port is not None else HTTP_PORT
        self.source_address = source_address
        self.sock = None
        self.timeout = timeout

    def request(self, method, url, body=None, headers={}):
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
        _HTTPConnectionInterface.__init__(self, host, port, timeout, source_address)
        transport._ProtocolInterface.__init__(self)

    def __del__(self):
        self.close()

    # Is this needed here, or only in HTTPResponse?
    def on(self, event):
        pass

class HTTPSConnection(HTTPConnection):
    def __init__(self, host, port=None, timeout=None, source_address=None, context=None, check_hostname=None):
        pass
