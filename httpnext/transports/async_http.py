import asyncio
from asyncio import get_event_loop, sleep, coroutine, Future

class _ProtocolInterface(asyncio.Protocol):
    def __init__(self):
        self._loop = get_event_loop()
        self._conn = None

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

    def _send_body(self):
        self._ready_to_send_body = Future()
        self._loop.run_until_complete(self._ready_to_send_body)
        self._loop.run_until_complete(self._send_body_coro())
        self._done = Future()

        self._loop.run_until_complete(self._done)

    @coroutine
    def _send_body_coro(self):
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
