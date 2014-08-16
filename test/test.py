#!/usr/bin/env python
# coding: utf-8

from __future__ import print_function, unicode_literals

import os
import sys
import unittest
import collections
import copy
import re

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from httpnext import *

class TestHTTPNext(unittest.TestCase):
    def test_basic_httpnext(self):
        c = HTTPConnection("localhost", 9000)
        c.connect()
        response = c.request("POST", "/", headers={"foo": "bar", "wat": "wat"}, body=b"0123456789ABCDEF"*1024)
        print("Got response:", response)

if __name__ == '__main__':
    unittest.main()
