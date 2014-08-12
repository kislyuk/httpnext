
* [RFC7230 - HTTP/1.1: Message Syntax and Routing - low-level message parsing and connection management](http://tools.ietf.org/html/rfc7230)
* [RFC7231 - HTTP/1.1: Semantics and Content - methods, status codes and headers](http://tools.ietf.org/html/rfc7231)
* [RFC7232 - HTTP/1.1: Conditional Requests - e.g., If-Modified-Since](http://tools.ietf.org/html/rfc7232)
* [RFC7233 - HTTP/1.1: Range Requests - getting partial content](http://tools.ietf.org/html/rfc7233)
* [RFC7234 - HTTP/1.1: Caching - browser and intermediary caches](http://tools.ietf.org/html/rfc7234)
* [RFC7235 - HTTP/1.1: Authentication - a framework for HTTP authentication](http://tools.ietf.org/html/rfc7235)

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
* HTTP parsing without establishing a connection
* Incremental HTTP parsing
* Raw socket control
