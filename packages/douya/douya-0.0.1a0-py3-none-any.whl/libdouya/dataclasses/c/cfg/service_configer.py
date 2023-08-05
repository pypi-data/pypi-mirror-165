# -*- coding:utf-8 -*-
#!/usr/bin/env python

from abc import abstractmethod
import typing
from ...i.srv import IDyService
from ..db.databases import Databases
from .parent.base_configer import BaseConfiger

class ServiceConfiger(BaseConfiger):
    def __init__(self):
        BaseConfiger.__init__(self)

    @abstractmethod
    def group_services(self, dbs: Databases) -> typing.Iterable[typing.List[IDyService]]:
        pass