* https://www.ietf.org/rfc/rfc2616.txt
* https://github.com/KeepSafe/aiohttp/blob/master/aiohttp/client.py
* https://github.com/python/cpython/blob/master/Lib/http/client.py
* https://github.com/joyent/node/blob/master/lib/_http_client.js
* https://github.com/lukasa/hyper - SPDY, HTTP2
* https://idea.popcount.org/2014-04-03-bind-before-connect/

# Features
* Early error support ([HTTP/1.1 8.2.3](http://www.w3.org/Protocols/rfc2616/rfc2616-sec8.html#sec8.2.3) `Expect: 100-continue`)
* Mid-stream error support
* Chunked i/o, event support
* Zero-length chunk keepalive
* asyncio.IncompleReadError.expected is the total expected size, not the remaining size
