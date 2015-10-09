#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author  : lhr (airhenry@gmail.com)
# @Link    : http://about.me/air.henry


from jinja2 import Template
from commutils.cli import subprocess,shlex,os,subprocess_run,subprocess_check_run,register_maker,run

import  six
if six.PY2:
    import sys
    reload(sys)
    sys.setdefaultencoding('utf8')

project={
    'name':'commutils',
    'author':'lhr',
    'author_email':'airhenry@gmail.com',
    'git_account':'lhrkkk'
}


register,_functions=register_maker()

@register
def project_gen():
    # 拷贝一份并重命名project_name
    subprocess_run("rm -rf target")
    subprocess_run("mkdir target")
    subprocess_run("cp -rf template/project target/")
    subprocess_run("mv target/project/project target/project/%s"%project['name'])
    subprocess_run("mv target/project target/%s"%project['name'])


    # 对于新的拷贝
    project_path = os.path.join("target",project['name'])

    for root,dirs,files in os.walk(project_path):
        # print root,dirs,files, '\n\n'
        for file in files:
            with open(os.path.join(root,file),'r') as f:
                s=Template(f.read()).render(project=project)
            with open(os.path.join(root,file),'w') as f:
                f.write(s)



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


if __name__ == '__main__':
    pass










## ===== start =========

# 初始化配置

# project_json='''
# {
# 'name': 'new'
#
# }
# '''
#
#
# class Project(object):
#     def __init__(self):
#         self.x=0
#
# import json
# project=Project()


# print(json.loads(project_json))
# project.__dict__=json.loads(project_json)


# print (project.__dict__)
#
# exit(0)

# class的__dict__只是字段, 并且可以直接赋值. 和字典一样. json.dumps(c.__dict__), c.__dict__=json.loads(s), 就可以

# class Project(dict):
#     def __init__(self):
#         pass
#
# project=Project()

#  todo: python字典和对象


