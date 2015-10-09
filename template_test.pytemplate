#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author  : lhr (airhenry@gmail.com)
# @Link    : http://about.me/air.henry


import unittest

from {{module_path}} import {{module_name}}

class Test{{module_name.capitalize()}}(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

{% for func_name,func_definition in all_functions  %}
    def test_{{ func_name }}(self):
        return
        {{ module_name}}.{{func_definition}}

{% endfor %}

if __name__ == '__main__':
    unittest.main()




