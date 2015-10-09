#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author  : lhr (airhenry@gmail.com)
# @Link    : http://about.me/air.henry



from __future__ import print_function
from commutils.cli import register_maker,run, subprocess_run,wrapper_decorator
from commutils.project_gen import project_gen
import functools

import os
import re
import inspect,importlib
from jinja2 import Template

register,_functions=register_maker()

@register
def gy():
    pass

def check_setup_py_origin(f):
    ## 保持原函数的__doc__和__name__

    @functools.wraps(f)
    @autokwoargs
    # 这里不能用*args, **kwargs, 因为clize不支持这样的函数头部.
    def wrapper(*args, **kwargs):
        print ('=============================')
        print (os.path.abspath('.'))
        print(os.path.exists('setup.py'))
        if not os.path.exists('setup.py'):
            print('ERROR: setup.py do not exist. Please check your path.')
            exit(0)
        else:
            return f(*args,**kwargs)
    return wrapper

## 用这个版本可以和clize一起正确处理*args, **kwargs, 另外函数不一定要return.
@wrapper_decorator
def check_setup_py(f,*args,**kwargs):
    if not os.path.exists('setup.py'):
        print('ERROR: setup.py do not exist. Please check your path.')
    else:
        return f(*args,**kwargs)


## register放在最后, 这样才能被clize访问到最终的函数
@register
@check_setup_py
def build():
    '''
    hello
    :return:
    '''
    command='python setup.py sdist'
    subprocess_run(command)

@register
@check_setup_py
def install():
    command='python setup.py install --prefix=~/.local'
    subprocess_run(command)

@register
@check_setup_py
def upload(test=False):
    if test:
        command='python setup.py sdist upload -r testpypi '
        subprocess_run(command)
    else:
        command='python setup.py sdist upload -r pypi '
        subprocess_run(command)



@register
@check_setup_py
def pip_install(test=False):
    command="pip install -i https://pypi.python.org/pypi commutils --user --upgrade"
    subprocess_run(command)

@register
@check_setup_py
def detox():
    command='detox'
    subprocess_run(command)


# todo: 学习记录

@register
@check_setup_py
def init_test():

    package_dir="commutils"
    unit_test_dir=os.path.join(package_dir,"tests/unit")

    exclude_dir=set(['tests','target','template','__pycache__'])
    py_pattern=re.compile(r'^(?!__init__).*\.py$')
    replace_pattern=re.compile(r'^%s'%package_dir)
    for root,dirs,files in os.walk(package_dir,topdown=True):
        # 本地修改, 另外列表生成式里面的变量不是局域的, 在用完后会保留.
        dirs[:] = [d for d in dirs if d not in exclude_dir]
        files[:] = [f for f in files if py_pattern.match(f)]
        print(root,dirs,files)
        for file in files:
            py_file=os.path.join(root,file)
            # test_file=os.path.join(root.replace(package_dir,unit_test_dir),'test_'+file)
            test_root=re.sub(replace_pattern,package_dir+"/tests/unit",root)
            test_file=os.path.join(test_root,'test_'+file)
            # print (test_file)
            if not os.path.exists(test_file):
                module=py_file.replace('.py','')
                module=module.replace('/','.')
                module_path=root.replace('/','.')
                module_name=file.replace('.py','')

                # done: 直接从文件内容里面提取函数名和函数头部
                # all_functions=[(func_name,func_definition),]

                definition_pattern=re.compile(r'^\s*def\s+((.*?)\(.*\))\s*:\s*$',re.M)
                with open(py_file) as f:
                    content=f.read()
                all_functions=definition_pattern.findall(content)
                all_functions=[(j,i) for (i,j) in all_functions]

                # 使用import module & inspect 的方法获取func_name和func_definition
                # imported_module=importlib.import_module(module)
                # all_functions = inspect.getmembers(imported_module, inspect.isfunction)
                # definition_pattern=re.compile(r'def (.*):')
                # all_functions=[(i[0],definition_pattern.search(inspect.getsource(i[1])).group(1)) for i in all_functions]



                if not os.path.exists(test_root):
                    os.makedirs(test_root)

                with open(os.path.join(unit_test_dir,'template_test.py')) as f:
                    content=Template(f.read()).render(module_path=module_path,module_name=module_name,all_functions=all_functions)
                # print content

                with open(test_file,'w') as f:
                    f.write(content)

# project_gen=register(project_gen)
@register
def pg():
    project_gen()

def manage():
    # alternative分派, 默认分派是函数名, 用字典可以修改默认分派名, 用@kwoargs可以对关键字参数进行分派
    # run(hello_world,alt={"vvv":version, "no_capitalized":hello_world})

    # 分派必须显示说明, 可以传入列表
    description="""
    python project manager
    """
    # todo: 改进: 按字典键排序生成值的列表.
    commands=_functions
    run(commands,description=description)

# todo: 模板,

if __name__ == '__main__':
    manage()


