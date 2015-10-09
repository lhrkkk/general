#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author  : lhr (airhenry@gmail.com)
# @Link    : http://about.me/air.henry
# subprocess: https://docs.python.org/2.6/library/subprocess.html
# sh: https://amoffat.github.io/sh/#interactive-callbacks
# clize: http://clize.readthedocs.org/en/3.0/why.html

from __future__ import print_function
import os,sh
import subprocess
import shlex
from six import StringIO

# todo: 解决python3和doc的问题. python3对中文的支持好. macro写好. rest, eve, 启动服务控制.
# todo: pbr 版本号
# from Queue import Queue
from sigtools.modifiers import autokwoargs,kwoargs
from sigtools.wrappers import wrapper_decorator
from clize import run

## ===========
## register装饰器
class Register():
    '''
    register的对象版本, register, functions对应装饰器, _function, 都是引用

    用例:
    reg=Register()

    _functions=reg.functions()
    register=reg.register

    @register
    def new():
        pass

    @register
    def new2():
        pass

    print(_functions)
    '''
    def __init__(self):
        self._functions={}

    # @staticmethod
    def register(self,f):
        self._functions[f.__name__]=f
        return f
    def functions(self):
        return self._functions

def register_maker():
    '''
    register的闭包版本, 返回两个值, 第一个是register, 第二个是_functions
    :return:

    用例:
    register,_functions=register_maker()

    @register
    def new():
        pass

    @register
    def new2():
        pass

    print (_functions)
    '''
    _functions={}
    def register(f):
        _functions[f.__name__]=f
        return f
    return register,_functions

def subprocess_run(command):
    return subprocess.call(shlex.split(command))
def subprocess_shell(command):
    return subprocess.Popen(command,shell=True)

def subprocess_check_run(command):
    return subprocess.check_call(shlex.split(command))

