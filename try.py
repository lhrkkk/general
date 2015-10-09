#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author  : lhr (airhenry@gmail.com)
# @Link    : http://about.me/air.henry


def register_maker():
    _functions={}
    def register(f):
        _functions[f.__name__]=f
        return f
    return register,_functions




if __name__ == '__main__':
    pass


