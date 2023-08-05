# -*- coding:utf-8 -*-
#!/usr/bin/env python

import warnings
from dataclasses import dataclass
from typing import List, Dict, Any, Tuple, Type, ClassVar
from ...utilities.singleton import singleton_d

@dataclass
class TypeInfo(object):
    original: Type
    alias_urls : List[str]

class naming_d(object):
    '''命名对象注解
    '''
    type_info : ClassVar[Dict[str, List[Tuple[Type, Dict[str, Any]]]]] = {}
    alias_info : ClassVar[Dict[str, str]] = {}

    def __init__(self, *names:str, is_singleton:bool = None, alias_urls:List[str] = None):
        self.__names = names
        self.__is_singleton = True if is_singleton else False
        self.__alias_urls = alias_urls if alias_urls else []

    def __call__(self, cls: Type) -> Type:
        # print(f'# {self} #', cls, ",", self.__names,  ",", self.__is_singleton,  ",", self.__alias_urls)
        cls_name =  f'{cls.__module__}:{cls.__name__}'
        cls_ = singleton_d(cls) if self.__is_singleton else cls
        all_names = [ cls_name, *self.__names ]

        for name in all_names:
            if name not in self.type_info: self.type_info.update({ name : [] })
            self.type_info[name].append((cls_, TypeInfo(original = cls, alias_urls = self.__alias_urls)))

        for alias_url in self.__alias_urls:
            if old_class_name := self.alias_info.get(alias_url):
                warnings.warn(f"Replace {alias_url} from '{old_class_name}' to '{cls_name}'")
            self.alias_info.update({ alias_url : cls_name })

        # print(f'# {self} #', self.type_info)
        # print(f'# {self} #', self.alias_info)

        return cls

class obj_d(naming_d):
    '''普通对象注解
    '''
    def __init__(self, *names:str, alias_urls:List[str] = None):
        naming_d.__init__(self, *names, is_singleton = False, alias_urls = alias_urls)

class svc_d(naming_d):
    '''服务型对象注解
    '''
    def __init__(self, *names:str, alias_urls:List[str] = None):
        naming_d.__init__(self, *names, is_singleton = True, alias_urls = alias_urls)