# -*- coding:utf-8 -*-
#!/usr/bin/env python

from typing import Dict,Any
from ...i.srv import IDyService
from ..db import Databases

class BaseAsyncService(IDyService):
    def __init__(self):
        IDyService.__init__(self)
        self.__configuration = None
        self.__code = None
        self.__dbs = None

    def __await__(self):
        yield from self.serve()

    @property
    def databases(self) -> Databases:
        return self.__dbs
    @databases.setter
    def databases(self, dbs:Databases):
        self.__dbs = dbs

    @property
    def configuration(self) -> Dict[str,Any]: 
        return self.__configuration or {}
    @configuration.setter
    def configuration(self, configuration:Dict[str, Any]):
        self.__configuration = configuration

    @property
    def code(self) -> str:
        return self.__code
    @code.setter
    def code(self, code:str):
        self.__code = code

    @property
    def parallel_mode(self) -> str:
        return self.configuration.get('parallel_mode', "mt")
    @parallel_mode.setter
    def parallel_mode(self, parallel_mode:str):
        self.configuration.update(parallel_mode = parallel_mode)

    @property
    def parallel_number(self) -> str:
        return int(self.configuration.get('parallel_number', 1))
    @parallel_number.setter
    def parallel_number(self, parallel_number:int):
        self.configuration.update(parallel_number = parallel_number)

    @property
    def schedule_configuration(self) -> Dict[str,Any]:
        return self.configuration.get('schedule', {})
    @schedule_configuration.setter
    def schedule_configuration(self, schedule_configuration:Dict[str,Any]):
        self.configuration.update('schedule', schedule_configuration)

    async def initialize(self):
        pass