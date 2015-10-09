#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author  : lhr (airhenry@gmail.com)
# @Link    : http://about.me/air.henry
class Register():
    def __init__(self):
        self._functions={}

    # @staticmethod
    def register(self,f):
        self._functions[f.__name__]=f
        return f
    def functions(self):
        return self._functions


if __name__ == '__main__':
    pass


