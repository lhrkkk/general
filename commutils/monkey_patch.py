#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author  : lhr (airhenry@gmail.com)
# @Link    : http://about.me/air.henry

# import functools

def as_method_of(cls):
    def as_method_of_cls(func):
        setattr(cls,func.__name__,func)
    return as_method_of_cls
def as_staticmethod_of(cls):
    def as_method_of_cls(func):
        setattr(cls,func.__name__,staticmethod(func))
    return as_method_of_cls

if __name__ == '__main__':
    pass


