# -*- coding:utf-8 -*-
#!/usr/bin/env python

from attrbox import AttrDict
from ....i.cfg import IBaseConfiger

class BaseConfiger(IBaseConfiger):
    def __init__(self):
        self.__configuration : AttrDict  = None

    def __enter__(self):
        return self

    def __exit__(self,exc_type, exc_val, exc_tb):
        pass

    @property
    def configuration(self) -> AttrDict:
        return self.__configuration
    @configuration.setter
    def configuration(self, configuration:AttrDict) -> AttrDict:
        self.__configuration = configuration

    def initialize(self, *args, **kwargs):
        pass