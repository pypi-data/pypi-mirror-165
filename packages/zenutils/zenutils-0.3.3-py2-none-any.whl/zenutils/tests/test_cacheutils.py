#!/usr/bin/env python
# -*- coding: utf8 -*-
from __future__ import absolute_import, division, generators, nested_scopes, print_function, unicode_literals, with_statement
from zenutils.sixutils import *
from zenutils import cacheutils

import random
import unittest

_test_cacheutils_counter = 0

class Object(object):
    pass

class TestCacheUtils(unittest.TestCase):

    def test01(self):
        a = Object()
        def hi():
            return "hi"
        assert cacheutils.get_cached_value(a, "hi", hi) == "hi"

    def test02(self):
        global _test_cacheutils_counter
        _test_cacheutils_counter = 0
        a = Object()
        def counter():
            global _test_cacheutils_counter
            _test_cacheutils_counter += 1
            return _test_cacheutils_counter
        assert cacheutils.get_cached_value(a, "counter", counter) == 1
        assert cacheutils.get_cached_value(a, "counter", counter) == 1

    def test03(self):
        a = Object()
        @cacheutils.cache(a, "_num")
        def getNum():
            return random.randint(1, 10)
        v1 = getNum()
        v2 = getNum()
        v3 = getNum()
        assert v1
        assert v1 == v2 == v3

    def test04(self):
        @cacheutils.cache(None, "_num")
        def getNum():
            return random.randint(1, 10)

        a = Object()
        v1 = getNum(a)
        v2 = getNum(a)
        v3 = getNum(a)
        assert v1
        assert v1 == v2 == v3

    def test5(self):
        @cacheutils.cache()
        def getNum():
            return random.randint(1, 10)
        a = Object()
        v1 = getNum(a, "_num")
        v2 = getNum(a, "_num")
        v3 = getNum(a, "_num")
        assert v1
        assert v1 == v2 == v3
