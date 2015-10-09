#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author  : lhr (airhenry@gmail.com)
# @Link    : http://about.me/air.henry


import unittest

from commutils.project_gen import project_gen

class TestProject_gen(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass


    def test_subprocess_run(self):
        return
        project_gen.subprocess_run(command)


    def test_subprocess_check_run(self):
        return
        project_gen.subprocess_check_run(command)


    def test_new(self):
        return
        project_gen.new(a,b=1,**kwargs)


    def test_project_gen(self):
        return
        project_gen.project_gen()



if __name__ == '__main__':
    unittest.main()



