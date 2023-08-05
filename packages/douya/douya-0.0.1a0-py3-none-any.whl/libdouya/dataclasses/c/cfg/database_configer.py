# -*- coding:utf-8 -*-
#!/usr/bin/env python

from abc import abstractmethod
from typing import Any
from attrbox import AttrDict
from ...i.rdb import IDatabaseDeclarative, IDatabases
from .parent.base_configer import BaseConfiger

class DatabaseConfiger(BaseConfiger):
    def __init__(self):
        BaseConfiger.__init__(self)

    @abstractmethod
    def initialize_and_get_databases(self, *declaratives:IDatabaseDeclarative) -> IDatabases:
        '''初始化并返回一个databases对象
        '''

    @abstractmethod
    def establish_connection(self, databases: IDatabases):
        '''确保databases对象的连接，当多进程时此方法可以确保子进程的数据库连接可用
        '''