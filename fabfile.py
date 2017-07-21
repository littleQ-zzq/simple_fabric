# -*- coding: utf-8 -*-
__author__ = "zhangzhenquan"

"""
此代码用于：
1. 多服务器 fabric 自动部署

数据来源：
1.

注意事项：
1.

调用方法：

"""
from fabric.api import *

WORK_PATH = "/opt/services"
CODE_PATH = "/opt/services/MyProject"
CONFIG_PATH = "/opt/services/MyProject/config"
GIT_CLONE_COMMAND = "git clone git@github.com:littleQ-zzq/simple_fabric.git"

MG_TEST_HOSTS = [
    'centos@IP1:22',
    'centos@IP2:22'
]
MG_UAT_HOSTS = [
    'centos@IP3:22',
    'centos@IP4:22',
    'centos@IP5:22'
]
MG_WUXIA_HOSTS = [
    'centos@IP6:22',
    'centos@IP7:22',
    'centos@IP8:22'
]
MG_WUXIB_HOSTS = [
    'centos@IP9:22',
    'centos@IP10:22',
    'centos@IP11:22'
]

MG_TEST_PASSWORD = "password1"
MG_UAT_PASSWORD = "password2"
MG_ONLINE_PASSWORD = "password3"

# 按环境分组
env.roledefs = {
    'mg_test': MG_TEST_HOSTS,
    'mg_uat': MG_UAT_HOSTS,
    'mg_wuxiA': MG_WUXIA_HOSTS,
    'mg_wuxiB': MG_WUXIB_HOSTS
}

# 设置服务器密码
env.passwords = {
    "centos@IP1:22": MG_TEST_PASSWORD,
    "centos@IP2:22": MG_TEST_PASSWORD,
    "centos@IP3:22": MG_UAT_PASSWORD,
    "centos@IP4:22": MG_UAT_PASSWORD,
    "centos@IP5:22": MG_UAT_PASSWORD,
    "centos@IP6:22": MG_ONLINE_PASSWORD,
    "centos@IP7:22": MG_ONLINE_PASSWORD,
    "centos@IP8:22": MG_ONLINE_PASSWORD,
    "centos@IP9:22": MG_ONLINE_PASSWORD,
    "centos@IP10:22": MG_ONLINE_PASSWORD,
    "centos@IP11:22": MG_ONLINE_PASSWORD,
}

# 异常预警处理
env.warn_only = True
# 并行执行
env.parallel = True


def pull_newest_code():
    """
    拉取最新代码
    :return:
    """
    with cd(WORK_PATH):
        run('rm -rf simple_fabric')
        run(GIT_CLONE_COMMAND)


def checkout_branch(branch_name):
    """
    切换分支
    :param branch_name:
    :return:
    """
    with cd(CODE_PATH):
        run('git checkout %s' % branch_name)


def update_config(config_name):
    """
    更新配置文件
    :param config_name:
    :return:
    """
    with cd(CONFIG_PATH):
        run('> config.py')
        run('cat %s >> config.py' % config_name)
        run('ls -al')


def restart_service():
    """
    重启服务
    :return:
    """
    run('sudo stop uwsgi')
    run('sudo /etc/init.d/nginx stop')
    run('sudo start uwsgi')
    run('sudo /etc/init.d/nginx start')


# --------------------------------------------------测试--------------------------------------------------
def test():
    print 'this is a fab test'


@roles('mg_test')
def mg_test():
    pull_newest_code()
    checkout_branch('backup_branch')


# --------------------------------------------------正常分支代码------------------------------------------
@roles('mg_uat')
def uat_deploy():
    """
    uat 部署
    :return:
    """
    pull_newest_code()
    checkout_branch('uat_usergrid')
    # restart_service()


@roles('mg_wuxiA')
def a_deploy():
    """
    wuxiA 部署
    :return:
    """
    pull_newest_code()
    checkout_branch('wuxiA_master')
    update_config('config_wuxiA.py')
    # restart_service()


@roles('mg_wuxiB')
def b_deploy():
    """
    wuxiB 部署
    :return:
    """
    pull_newest_code()
    checkout_branch('wuxiB_master')
    update_config('config_wuxiB.py')
    # restart_service()


# --------------------------------------------------备份分支代码-------------------------------------------
@roles('mg_uat')
def backup_uat_deploy():
    """
    uat backup_branch 部署
    :return:
    """
    pull_newest_code()
    checkout_branch('backup_branch')
    # restart_service()


@roles('mg_wuxiA')
def backup_a_deploy():
    """
    wuxiA backup_branch 部署
    :return:
    """
    pull_newest_code()
    checkout_branch('backup_branch')
    update_config('config_wuxiA.py')
    # restart_service()


@roles('mg_wuxiB')
def backup_b_deploy():
    """
    wuxiB backup_branch 部署
    :return:
    """
    pull_newest_code()
    checkout_branch('backup_branch')
    update_config('config_wuxiB.py')
    # restart_service()
