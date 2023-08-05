# -*- coding:utf-8 -*-
#!/usr/bin/env python

'''
    env_defs.py - 环境变量相关
'''

from enum import Enum,unique

@unique
class EnvDefs(Enum):
    # 加载扫描的模块，搭配命名注解使用，多个模块用分号分隔。
    APP_MODULE = 0

    # 定义程序的工作根目录，该变量可以改变程序工作目录。
    APP_WORK_DIR = 1

    # 定义应用环境配置，如：dev,prod。该变量会影响加载环境配置文件的读取。
    APP_ENV = 2

    # 定义程序的配置路径，多个路径使用冒号分割。该变量是程序扫描配置文件时的路径集合。
    APP_CFG_DIR = 3

    # 定义程序的配置文件名字。多个配置文件，使用冒号分割。加载顺序是后面配置覆盖前面的配置。
    APP_CFG_NAME = 4

    # 定义程序的除配置路径以外的，其他扩展检查路径，多个路径使用冒号分割。该变量是程序扫描文件时的路径集合。最终扫描路径来源是配置路径和该值的叠加
    APP_LOOKUP_DIR = 5

    # 定义程序的网络地址。改此变量会修改程序监听地址，包括且不限于HTTP/GRPC。
    APP_HOST = 6

    # 定义程序的HTTP端口。改此变量会影响程序HTTP监听端口。
    APP_PORT = 8

    # 定义数据库连接地址信息
    APP_DB_URL = 9

    # 定义数据目录地址
    APP_CATALOG_DATA_DIR = 10

@unique
class EnvFilterModeDef(Enum):
    #扫描所有文件，包括原文件和环境文件
    ALL = 1
    #仅扫描环境文件
    ONLY_ENV_FILES = 2
    #仅扫描环境文件
    EXINCLUDING_ENV_FILES = 3
    #环境文件优先
    ENV_FILES_FIRST = 4

@unique
class EnvSelectModeDef(Enum):
    #选出任一文件
    ANY = 0
    #选出所有文凭
    ALL = 1