# -*- coding:utf-8 -*-
#!/usr/bin/env python

"""
    singleton.py -  单例模式类
"""

import threading

class singleton_d(object):
    '''
    单例的装饰器
    用法说明：
    @singleton_d
    class MyClass():
        def __init__(self, ...):
            pass

    o1 = MyClass(...)
    o2 = MyClass(...)
    assert(o1 == o2)
    '''
    def __init__(self, cls):
        self.__cls = cls
        self.__singleton_info__ = {}

    def __call__(self):
        print(f"# {self} #", self.__cls, self.__singleton_info__)
        if self.__cls not in self.__singleton_info__:
            self.__singleton_info__[self.__cls] = self.__cls()
        return self.__singleton_info__[self.__cls]

class Singleton(type):
    '''
    用法说明:
    class MyClass(ParentClass, metaclass=Singleton):
        def __init__(self, ...):
            pass

    o1 = MyClass(...)
    o2 = MyClass(...)
    assert(o1 == o2)
    '''
    def __init__(self, *args, **kwargs):
        super(Singleton, self).__init__(*args, **kwargs)
        self.__singleton_locker__ = threading.Lock()
        self.__singleton__ = None

    def __call__(cls, *args, **kwargs):
        if not cls.__singleton__:
            with cls.__singleton_locker__:
                if not cls.__singleton__:
                    cls.__singleton__ = super(Singleton, cls).__call__(*args, **kwargs)
        return cls.__singleton__

    '''
    def __new__(cls, name, bases, attrs):
        attrs["get_instance"] = classmethod(lambda c: c())
        return super(Singleton, cls).__new__(cls, name, bases, attrs)
    '''