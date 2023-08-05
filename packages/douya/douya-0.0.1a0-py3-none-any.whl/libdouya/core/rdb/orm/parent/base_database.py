# -*- coding:utf-8 -*-
#!/usr/bin/env python

from abc import abstractmethod
import logging, typing, threading, os
from .....definations.db import OptDef, OrmConnectionPoolTypeDef
from .....dataclasses.i.rdb import IDatabaseDeclarative, IDatabaseProxy

class BaseDatabaseDeclarative(IDatabaseDeclarative):
    def __init__(self, code_name:str):
        IDatabaseDeclarative.__init__(self)
        self.__code_name = code_name

    @property
    def code_name(self) -> str:
        return self.__code_name

class BaseDatabaseProxy(IDatabaseProxy):
    def __init__(self, code_name:str, declarative: IDatabaseDeclarative, **configuration: typing.Any):
        IDatabaseProxy.__init__(self)
        self.__code_name = code_name
        self.__declarative = declarative
        self.__configuration = configuration.copy()

        self.__initialization_flag_lock = threading.Lock()
        self.__initialization_flag_set = set()

    @property
    def code_name(self) -> str:
        return self.__code_name

    @property
    def configuration(self) -> typing.Dict[str, typing.Any]:
        return self.__configuration or {}

    @property
    def connection_url(self) -> str:
        '''数据库链接
        形如： dialect+driver://username:password@host:port/database
        '''
        return self.configuration.get('url', "sqlite:///:memory:")

    @property
    def connection_options(self) -> typing.List[str]:
        return self.configuration.get('options', [OptDef.CREATING_TABLES.value])

    @property
    def is_debugging(self) -> bool:
        return bool(self.configuration.get('is_debugging', False))

    @property
    def declarative(self) -> IDatabaseDeclarative:
        return self.__declarative

    @abstractmethod
    def get_orm_connection_pool_type(self) -> str:
        '''连接池类型
        '''

    def __gen_current_initialization_flag(self) -> str:
        cpt = self.get_orm_connection_pool_type()
        if OrmConnectionPoolTypeDef.ONLY_ONE.value == cpt:
            return "1"
        elif OrmConnectionPoolTypeDef.EVERY_THREAD.value == cpt:
            return f"{os.getpid()}:{threading.current_thread().ident}"
        else:
            return f"{os.getpid()}"

    def __establish_connection_internally(self, enable_scheme_rebuiding:bool):
        flag = self.__gen_current_initialization_flag()
        if flag not in self.__initialization_flag_set:
            with self.__initialization_flag_lock:
                if flag not in self.__initialization_flag_set:
                    try:
                        self.connect(enable_scheme_rebuiding = enable_scheme_rebuiding)
                        self.__initialization_flag_set.add(flag)
                    except:
                        logging.exception(f"Connect '{self.code_name}' database failed")

    def establish_connection(self):
        self.__establish_connection_internally(False)

    def initialize(self):
        # 为了初始化数据库样式，创建时，需要立刻进行一次初始化。
        # enable_scheme_rebuiding = False if self.__initialization_flag_set else True
        self.__establish_connection_internally(True)

