# -*- coding:utf-8 -*-
#!/usr/bin/env python

from typing import List
from .naming import obj_d
from ..utilities.configer import make_configer_url

class configer_d(obj_d):
    '''配置对象注解
    '''
    def __init__(self, key:str, *names:str):
        obj_d.__init__(self, *names, alias_urls = [make_configer_url(key)])

    # def __call__(self, callable: Callable,  *args: Any, **kwargs: Any) -> Any:
    #     # all_shortcuts = [f'{callable.__module__}:{callable.__name__}', *self.__shortcuts]
    #     # for sc in all_shortcuts:
    #     #     self.ALL_CONFIGER_INFO.update({ sc :  (self.__path, callable) })
    #     return named.__call__(self, callable, *args, **kwargs)