# -*- coding:utf-8 -*-
#!/usr/bin/env python

from abc import abstractmethod
from typing import List
from ...i.datacache import IDatacache
from .parent.base_configer import BaseConfiger

class DatacacheConfiger(BaseConfiger):
    def __init__(self):
        BaseConfiger.__init__(self)

    @abstractmethod
    def make_data_caches(self) -> List[IDatacache]:
        '''创建数据缓存对象列表
        '''