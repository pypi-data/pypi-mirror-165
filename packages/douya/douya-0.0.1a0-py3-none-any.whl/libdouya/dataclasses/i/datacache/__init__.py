# -*- coding:utf-8 -*-
#!/usr/bin/env python

from abc import ABCMeta, abstractmethod, abstractproperty
from typing import List, Any

class IDatacacheObjectBuilder(metaclass = ABCMeta):
    @abstractmethod
    def build(self) -> Any: pass

class IDatacache(metaclass = ABCMeta):
    @abstractproperty
    def id(self) -> Any: pass

    @abstractmethod
    def intialize(self): pass

    @abstractmethod
    def make_builder(self, key: Any) -> IDatacacheObjectBuilder: pass