# -*- coding:utf-8 -*-
#!/usr/bin/env python

from typing import Any, Dict
from ....utilities.singleton import Singleton
from ....dataclasses.i.datacache import IDatacache, IDatacacheObjectBuilder
from .error.error_datacache import ErrorDatacache

class DatacacheMgr(metaclass = Singleton):
    def __init__(self):
        self.__cache_info : Dict[str, IDatacache] = {}

    @staticmethod
    def get_instance() -> 'DatacacheMgr':
        '''
        由于是单例，所以调用构造函数永远都返回同一个实例
        '''
        return DatacacheMgr()

    def initialize(self):
        self.add(ErrorDatacache())

    def add(self, *datacaches : IDatacache):
        for datacache in datacaches:
            self.__cache_info.update({ datacache.id : datacache })

    def make_builder(self, id:str, key:Any) -> IDatacacheObjectBuilder:
        datacache: IDatacache = self.__cache_info.get(id)
        if not datacache: raise RuntimeError(f"No '{id}' datacahe found")

        return datacache.make_builder(key)