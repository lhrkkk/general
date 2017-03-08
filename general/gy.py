#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author  : lhr (airhenry@gmail.com)
# @Link    : http://about.me/air.henry


'''
本地流程就是分支内commit. 只要init, commit就行了

远程流程就是1.clone, checkout新分支, 2.commit, 3.与主干同步sync, 4.合并commit(rebase), 5.push到远程分支, 最后发出pull-request

对远程:
1. clone, 或者init_remote (init, create or add_remote, push), 注意第一个init最好要是空的, 之后再commit, push
2. 要提交到远端用branchpush做完之后的四步.

对于直接远程直接master开发: http://www.ruanyifeng.com/blog/2012/07/git.html
不要在master上面开发, master只做合并, 测试, 修bug.
开发用dev分支. 合并dev的时候可以不提交远程直接在本地合并, commit, rebase, merge,
或者用github的功能总是推到远程进行合并.


参考资料:
git 流程规范 http://www.ruanyifeng.com/blog/2015/08/git-use-process.html
gitlab flow http://www.ruanyifeng.com/blog/2015/12/git-workflow.html
git 教程   http://backlogtool.com/git-guide/cn/
force push的注意事项: http://willi.am/blog/2014/08/12/the-dark-side-of-the-force-push/

'''

from __future__ import print_function

## 解决utf8的问题
import six

from general.cli import (autokwoargs, os, register_maker,
                         run, sh, shlex, subprocess, subprocess_check_run,
                         subprocess_run, )

if six.PY2:
    import sys

    reload(sys)
    sys.setdefaultencoding('utf8')

register, _functions = register_maker()

already_commit=0


## ====================
## 基础任务

VERSION = 0.1


@register
def version(the_version=VERSION):
    """Show the version"""
    return '{0} version {1}'.format(__file__, the_version)


@register
@autokwoargs
def status():
    '''
    git status
    :return:
    '''
    os.system("git status")


@register
def init():
    '''
    init a new local repo.
    :return:
    '''
    # subprocess.call['git','init']
    if len(os.listdir('.')) == 0:
        subprocess.check_call(['touch', 'readme.md'])
    subprocess.check_call(['git', 'init'])
    commit(message='init commit')
    return "SUCCESS: inited a new project."


@register
def add_remote():
    '''
    add remote repo
    :return: the status whether successful
    '''
    project_name = os.path.basename(os.path.abspath('.'))
    # todo: 异常处理
    subprocess.call(['git', 'remote', 'add', 'origin', 'git@github.com:lhrkkk/%s.git' % project_name])
    subprocess.check_call(['git', 'remote', '-v'])
    return "SUCCESS: pushed to remote "


@register
def pull():
    '''
    wrapper for git pull
    :return:
    '''
    os.system('git pull')


@register
def reset():
    # todo: implement the reset
    '''
    :return:
    '''
    os.system("git reset")
    pass


@register
def reset_tree():
    # todo:
    os.system("git checkout -f HEAD")


@register
def diff():
    # todo: implement the diff
    '''
    :return:
    '''
    subprocess_check_run('git diff')


@register
def find_branch_name():
    return subprocess.check_output(shlex.split("git rev-parse --abbrev-ref HEAD")).strip().decode()


@register
@autokwoargs
def simplepush(force=False):
    '''
    push 当前分支到远端.
    :param force:
    :return:
    '''
    # git push --force origin myfeature
    branch_name = find_branch_name()
    if not force:
        subprocess.call(['git', 'push', '-u', 'origin', branch_name])
    else:
        subprocess.call(['git', 'push', '--force', 'origin', branch_name])

    return


@register
def log():
    '''
    彩图显示全局的分支和commit图
    :return:
    '''
    # subprocess_run("git log --graph --oneline --all")
    subprocess_run("git l --graph --date=short")


@register
def branch_is_exist(branch_name):
    # git rev-parse --verify <branch_name> # 返回值等于0的时候存在. 和下面命令等价
    command = "git show-ref --verify --quiet refs/heads/" + branch_name
    try:
        subprocess_check_run(command)
        return True
    except:
        return False


@register
def checkout(branch):
    subprocess_check_run("git checkout " + branch)


@register
def tag(tag_name):
    subprocess_check_run("git tag -a " + tag_name)
    return

@register
def amend(tag_name):
    os.system("git commit --amend" )
    return

@register
@autokwoargs
def master():
    checkout('master')
    # if merge:
    #     branch_merge_to('master')


## =================
## 主要部分

@register
def sync():
    '''
    sync remote changes to local branch.
    :return:
    '''
    # git fetch origin
    commit()
    subprocess.check_call(['git', 'fetch', 'origin'])
    # git rebase origin master
    subprocess.check_call(['git', 'rebase', 'origin/master'])
    return "SUCCESS: synced to remote repo."


@register
def rebase():
    # git rebase -i origin/master
    # 就用origin/master, rebase对比仓库的head
    commit()
    subprocess.check_call(['git', 'rebase', '-i', '--autosquash', 'origin/master'])
    return


## merge别人的code的时候往往会先在本地把master merge进分支进行合并, 成功后, 再把分支merge进master
@register
def merge(to_branch='master'):
    '''
    本地开发的小branch 直接merge进master, 不去远程merge了.
    :return:
    '''
    branch_name = find_branch_name()
    commit()
    sync()
    rebase()
    # subprocess_run("git merge "+to_branch)
    subprocess_run("git checkout " + to_branch)
    # print("git merge --no-ff "+branch_name)
    # print( shlex.split("git merge --no-ff "+branch_name))
    subprocess_run("git merge --no-ff " + branch_name)


## ==========
## 最主要流程

## 和别人合作步骤: 1.下载新建分支,clone, newbranch 2.提交*n, sync, branchpush(sync, rebase, push, ), 3. 发出pull-request
## 自己分支合并步骤: 1. 初始化init/初始化远程init_remote, 新建dev分支 2. 提交*n, 同步, rebase,(push) 3.merge
## 发布步骤:push


# commit, sync, (rebase), push/merge, 后一个必须有前一个作为前提.

# 最终就是, commit, sync, push/merge

@register
# @kwoargs('from_branch')
def switch(branch_name, from_branch='master'):
    '''
    from the newest master checkout a new branch named branch_name, 要先pull
    :param branch_name:
    :return:
    '''

    if not branch_is_exist(branch_name):
        subprocess.check_call(['git', 'checkout', from_branch])
        flag = 'y'
        try:
            subprocess.check_call(['git', 'pull'])
        except:
            print("ERROR: no remote source specified")
            flag = raw_input("Do you want to continue? [y(default)/n]:")
            # todo: 修改 new 为 switch 并且处理 remote 分支存在的问题.
        if flag == 'y' or flag == 'yes':
            subprocess.check_call(['git', 'checkout', '-b', branch_name])
            return "SUCCESS: new branch %s created and checked out" % branch_name
        else:
            return ("command canceled")
    else:
        flag = raw_input("Branch does not exist. Do you want to create a new one ? [y(default)/n]:")
        if flag == 'y' or flag == 'yes':

            subprocess.check_call(['git', 'checkout', branch_name])


@register
@autokwoargs
def commit(message=None):
    '''
    git add & commit all changes to local repo.
    :return:
    '''
    global already_commit
    if already_commit == 1:
        return
    already_commit = 1
    os.system("git status")
    input = raw_input("It will add and commit all changes and untracked files , continue? [y(default)/n]:")
    if input == "n":
        return ("commit canceled")

    os.system("git add .")
    if not message:
        status = subprocess.call(['git', 'commit'])
    else:
        status = subprocess.call(['git', 'commit', '-m', message])
    if status:
        return ("commit canceled")
    else:
        log_msg = '''
Summary of actions:
- git add .
- git commit
'''
        # print(log_msg)
        return ("Added and commited successfully.")


@register
@autokwoargs
def push(force=False):
    '''
    平时的时候应该维护dev的分支, 如果要merge到主分支的时候或者到push远程的时候, 则rebase成一个点.
    :return:
    '''
    # todo: 解决多重commit
    try:
        commit()
    except:
        pass
    sync()
    rebase()
    simplepush(force=force)


@register
def drop(branch):
    subprocess_run("git branch -d " + branch)


def main():
    # alternative分派, 默认分派是函数名, 用字典可以修改默认分派名, 用@kwoargs可以对关键字参数进行分派
    # run(hello_world,alt={"vvv":version, "no_capitalized":hello_world})

    # 分派必须显示说明, 可以传入列表
    description = '''
    主要用法

    gy new_branch ;
    gy commit ;
    gy push ;
    gy delete_branch ;

    次要用法

    gy sync ;
    gy rebase ;
    gy merge ;

    '''
    # commands = [i.__name__ for i in locals().values() if callable(i)]


    # import operator
    # todo: 改进: 按字典键排序生成值的列表.
    commands = _functions
    run(commands, description=description)


if __name__ == '__main__':
    main()
