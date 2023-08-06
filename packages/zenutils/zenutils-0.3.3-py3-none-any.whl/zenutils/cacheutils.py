#!/usr/bin/env python
# -*- coding: utf8 -*-
from __future__ import absolute_import, division, generators, nested_scopes, print_function, unicode_literals, with_statement
from zenutils.sixutils import *

import functools

__all__ = [
    "get_cached_value",
    "cache",
]

def get_cached_value(holder_object, cache_key, getter, *args, **kwargs):
    """Get cached value from an holder_object and set the cache value at the first request.

    @Returns:
        (Any): The cahced value or the getter returned value.
    
    @Parameters:
        holder_object(Any): The holder object which holds the cache property.
        cache_key(str): The cache property which will attach to the holder object.
        getter(Callable): The callable object which will be called if there is no cache value.
        *args(Any): Place holder parameters which will be used by getter.
        **kwargs(Any): Keyword parameters which will be used by getter.

    @Example:
        token = request.GET.get("token")
        value = get_cached_value(request, "cache_key_for_get_user_info", services.get_user_info, token=token)
    """
    cache_key = force_text(cache_key)
    if not hasattr(holder_object, cache_key):
        setattr(holder_object, cache_key, getter(*args, **kwargs))
    return getattr(holder_object, cache_key)

def cache(holder_object=None, cache_key=None):
    """
    @Notice:
        If your only give one parameter, then the parameter will be treated as cache_key.

    @Parameters:
        holder_object(Any): The holder object which holds the cache property.
        cache_key(str): The cache property which will attach to the holder object.

    @Example:
        a = Object()
        @cacheutils.cache(a, "_num")
        def getNum():
            return random.randint(0, 10)
        v1 = getNum()
        v2 = getNum()
        v3 = getNum()
        assert v1 == v2 == v3

    @Example
        @cacheutils.cache("_num")
        def getNum():
            return random.randint(0, 10)
        a = Object()
        v1 = getNum(a)
        v2 = getNum(a)
        v3 = getNum(a)
        assert v1 == v2 == v3

    @Example
        @cacheutils.cache()
        def getNum():
            return random.randint(0, 10)
        a = Object()
        v1 = getNum(a, "_num")
        v2 = getNum(a, "_num")
        v3 = getNum(a, "_num")
        assert v1 == v2 == v3
    """

    if holder_object and cache_key is None:
        cache_key = holder_object
        holder_object = None

    def outer(func):
        @functools.wraps(func)
        def inner(*args, **kwargs):
            # 当你在局部函数中修改某个变量的值时
            # 那这个变量就成了这个局部函数局部变量
            # 所以在这个变量被赋值前
            # 也无法继承宿主函数的变量值
            # 所以我们这里需要引入holder_object_inner
            # 这样以来在inner函数中就没有对holder_object变量的任何修改
            # 这时在inner函数中就可以取出宿主函数变量holder_object
            if (holder_object is None) and (cache_key is None):
                holder_object_inner = args[0]
                cache_key_inner = args[1]
                args = args[2:]
            elif holder_object is None:
                holder_object_inner = args[0] 
                cache_key_inner = cache_key
                args = args[1:]
            else:
                holder_object_inner = holder_object
                cache_key_inner = cache_key
            if hasattr(holder_object_inner, cache_key_inner):
                return getattr(holder_object_inner, cache_key_inner)
            else:
                result = func(*args, **kwargs)
                setattr(holder_object_inner, cache_key_inner, result)
                return result
        return inner
    return outer
