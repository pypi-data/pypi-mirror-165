# -*- coding:utf-8 -*-
#!/usr/bin/env python

from typing import Union, Any, List, Type
from ....utilities.singleton import Singleton
from ...deco import naming_d

class NamingMgr(metaclass = Singleton):
    def __init__(self):
        pass

    @staticmethod
    def get_instance() -> 'NamingMgr':
        '''
        由于是单例，所以调用构造函数永远都返回同一个实例
        '''
        return NamingMgr()

    def new_naming(self, what:Union[str, Type], *args:Any, **kwargs:Any) -> Any:
        if isinstance(what, Type):
            name =  f'{what.__module__}:{what.__name__}'
        else:
            name = str(what)

        if cls_name := naming_d.alias_info.get(name):
            name = cls_name

        cls_list = naming_d.type_info.get(name)
        if not cls_list:
            raise RuntimeError(f"Not found naming type: {name}")

        cls, _ = cls_list[-1]
        print(f'# {self} #', cls_list)
        return cls(*args, **kwargs)

    def get_alias_urls(self, what:Union[str, Type]) -> List[str]:
        if isinstance(what, type):
            name =  f'{what.__module__}:{what.__name__}'
        else:
            name = str(what)

        cls_list = naming_d.type_info.get(name)
        if not cls_list:
            raise RuntimeError(f"Not found naming type: {name}")

        _, opt = cls_list[-1]
        return opt.alias_urls