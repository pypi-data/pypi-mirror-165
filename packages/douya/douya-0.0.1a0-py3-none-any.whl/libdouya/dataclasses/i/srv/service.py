# -*- coding:utf-8 -*-
#!/usr/bin/env python

from abc import ABCMeta, abstractproperty, abstractmethod
from typing import Any, Dict
from ...c.db.databases import Databases

class IDyService(metaclass = ABCMeta):
    def __init__(self): pass

    @abstractproperty
    def databases(self) -> Databases:
        '''数据库对象'''
    @databases.setter
    @abstractmethod
    def databases(self, val: Databases):
        pass

    @abstractproperty
    def configuration(self) -> Dict[str, Any]:
        '''配置'''
    @configuration.setter
    @abstractmethod
    def configuration(self, val: Dict[str, Any]):
        pass

    @abstractproperty
    def code(self) -> str:
        '''唯一编码'''
    @code.setter
    @abstractmethod
    def code(self, val: str):
        pass

    @abstractproperty
    def parallel_mode(self) -> str:
        '''并发方式：mt/mp'''
    @parallel_mode.setter
    @abstractmethod
    def parallel_mode(self, val: str):
        pass

    @abstractproperty
    def parallel_number(self) -> int:
        '''并发数目'''
    @parallel_number.setter
    @abstractmethod
    def parallel_number(self, val: int):
        pass

    @abstractproperty
    def schedule_configuration(self) -> Dict[str,Any]:
        '''调度配置'''
    @schedule_configuration.setter
    @abstractmethod
    def schedule_configuration(self, val: Dict[str,Any]):
        pass

    @abstractmethod
    async def initialize(self): pass

    @abstractmethod
    async def serve(self): pass