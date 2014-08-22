import asyncio
from asyncio import get_event_loop, sleep, coroutine, Future

class _ProtocolInterface(asyncio.Protocol):
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

