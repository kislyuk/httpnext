#!/usr/bin/env python3
# coding: utf-8

from __future__ import absolute_import, division, print_function, unicode_literals

import os
import sys
import unittest
import collections
import copy
import re

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import httpnext
#from httpnext import *

class TestHTTPNext(unittest.TestCase):
    def test_basic_httpnext(self):
        #conn = httpnext.HTTPConnection("www.python.org")
        #conn.connect()
        #conn.request("GET", "/index.html")
        #r1 = conn.getresponse()
        #print(r1.status, r1.reason)
        #while not r1.closed:
        #    print(r1.read(200))

        c = httpnext.HTTPConnection("localhost", 9000)
        c.connect()
        c.request("POST", "/", headers={"foo": "bar", "wat": "wat"}, body=b"0123456789ABCDEF"*1024)
        print("Sent!")
        res = c.getresponse()
        #response = c.request("POST", "/", headers={"foo": "bar", "wat": "wat"}, body=b"0123456789ABCDEF"*1024)
        print("Got response:", res)

if __name__ == '__main__':
    unittest.main()
