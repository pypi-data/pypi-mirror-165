# -*- coding:utf-8 -*-
#!/usr/bin/env python

import logging
from urllib.parse import urlparse
from typing import Any,Dict
from contextlib import contextmanager

try:
    from sqlalchemy.ext.declarative import declarative_base, DeclarativeMeta
    from sqlalchemy.orm import Session,sessionmaker,scoped_session
    from sqlalchemy.engine import Engine
    from sqlalchemy import create_engine
except:
    pass
from ....definations.err import ErrorDefs
from ....definations.db import DialectDef, OptDef, OrmDef, OrmConnectionPoolTypeDef
from ....dataclasses.i.rdb import IDatabaseDeclarative, IDatabaseProxy
from ....dataclasses.c.err import DyError
from ...deco import obj_d
from .parent.base_database import BaseDatabaseDeclarative, BaseDatabaseProxy

class SqlAlchemyDatabase(BaseDatabaseProxy):
    def __init__(self, id:str, declarative: IDatabaseDeclarative, **configuration: Any):
        BaseDatabaseProxy.__init__(self, id, declarative, **configuration)
        self.__session_factory = None
        self.__engine = None

    def __get_session_factory(self) -> sessionmaker:
        if not self.__session_factory:
            self.__session_factory = sessionmaker(bind = self.__engine)
            if self.configuration.get('multi_threading'):
                self.__session_factory = scoped_session(self.__session_factory)
        return self.__session_factory

    @property
    def internal_implementation(self) -> Any:
        return self.__engine

    def get_orm_connection_pool_type(self) -> str:
        return OrmConnectionPoolTypeDef.EVERY_PROCESSOR.value

    def connect(self, enable_scheme_rebuiding:bool):
        connection_options = self.connection_options or []
        
        self.__engine = create_engine(self.url)
        if enable_scheme_rebuiding:
            if OptDef.DROPPING_TABLES.value in connection_options:
                self.declarative.internal_implementation.metadata.drop_all(self.__engine)
            if OptDef.CREATING_TABLES.value in connection_options:
                self.declarative.internal_implementation.metadata.create_all(self.__engine, checkfirst = True)
            # DbBase.metadata.drop_all(self.__engine)
            # DbBase.metadata.create_all(self.__engine, checkfirst = True)

    @contextmanager
    def on_session(self) -> Any:
        session_factory = self.__get_session_factory()
        yield session_factory()

    @contextmanager
    def on_transactional_session(self) -> Any:
        with self.on_session() as s:
            try:
                yield s
                s.commit()
            except BaseException as e:
                # logging.exception("Got some exception")
                s.rollback()
                raise DyError(ErrorDefs.DB_OPERATE_FAILED.value, "Operate Database Failed", str(e)).as_exception()

@obj_d(OrmDef.SQLALCHEMY_ORM.value)
class SqlAlchemyDatabaseDeclarative(BaseDatabaseDeclarative):
    def __init__(self):
        BaseDatabaseDeclarative.__init__(self)
        self.__base : DeclarativeMeta  = declarative_base()

    @property
    def table(self) -> Any:
        return self.__base

    @property
    def internal_implementation(self) -> Any:
        return self.__base

    def make_proxy(self, **configuration:Any) -> IDatabaseProxy:
        return SqlAlchemyDatabase(self.code_name, self, **configuration)