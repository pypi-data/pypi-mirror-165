# -*- coding:utf-8 -*-
#!/usr/bin/env python

import os, logging
from urllib.parse import urlparse
from typing import Any,Dict
from contextlib import contextmanager

try:
    from pony.orm import Database as DatabaseImplementation, sql_debug
    from pony.orm import commit as commit_session, rollback as rollback_session
    from pony.orm.core import db_session
except:
    pass
from ....definations.err import ErrorDefs
from ....definations.db import DialectDef, OptDef, OrmDef, OrmConnectionPoolTypeDef
from ....dataclasses.i.rdb import IDatabaseDeclarative, IDatabaseProxy
from ....dataclasses.c.err import DyError
from ...deco import obj_d
from .parent.base_database import BaseDatabaseDeclarative, BaseDatabaseProxy

class PonyDatabaseProxy(BaseDatabaseProxy):
    def __init__(self, code_name:str, declarative: IDatabaseDeclarative, **configuration: Any):
        BaseDatabaseProxy.__init__(self, code_name, declarative, **configuration)
        self.__session_factory = None
        # IDatabase.__init__(self, name, configuration)
        # self.__core = OrmDatabase()
        # self.__session_factory = None

    @property
    def internal_implementation(self) -> Any:
        return self.declarative.internal_implementation

    def get_orm_connection_pool_type(self) -> str:
        return OrmConnectionPoolTypeDef.ONLY_ONE.value

    def connect(self, enable_scheme_rebuiding:bool):
        '''需要确保线程可重复
        '''
        logging.info("All table entities : %s" % (','.join(([ f'{name}({entity})' for name, entity in self.internal_implementation.entities.items() ]))))

        connection_options = self.connection_options or []

        u = urlparse(self.connection_url)
        if u.scheme is None:
            raise RuntimeError(f"Invalid database url. No 'scheme' found : {self.url}")
        elif u.scheme.lower() == DialectDef.SQLITE.value.lower():
            if u.path in ['', '/', '/:memory:']:
                self.internal_implementation.bind(provider='sqlite', filename = ':memory:')
            else:
                db_dir = self.configuration.get("db_dir") or os.getcwd()
                db_file_path = os.path.abspath(os.path.join(db_dir, u.path[1:]))
                self.internal_implementation.bind(provider='sqlite', filename = db_file_path, create_db = True)
        elif u.scheme.lower() == DialectDef.PG.value.lower():
            # postgresql://scott:tiger@localhost:5432/mydatabase'
            opt = {}
            if u.path in ['', '/']: raise RuntimeError(f"Invalid database url. No 'database' found: {self.url}")
            if u.username: opt.update(user = u.username)
            if u.password: opt.update(password = u.password)
            if u.hostname: opt.update(host = u.hostname)
            if u.port: opt.update(port = u.port)
            # self.__core.bind(provider='postgres', user='testor', password='testor', host='10.19.156.28', port=30432, database='testdb')
            # db.bind(provider='mysql', host='', user='', passwd='', db='')
            # db.bind(provider='oracle', user='', password='', dsn='')
            self.internal_implementation.bind(provider='postgres', database=u.path[1:], **opt)
        else:
            raise RuntimeError(f"Unsupported database source: {self.connection_url}")

        if self.is_debugging:
            sql_debug(True)

        if enable_scheme_rebuiding and (OptDef.DROPPING_TABLES.value in connection_options):
            logging.info("Drop all tables")
            self.internal_implementation.drop_all_tables(with_all_data = True)

        if enable_scheme_rebuiding and (OptDef.CREATING_TABLES.value in connection_options):
            # self.internal_implementation.create_tables(check_tables = False)
            logging.info("Create all tables")
            self.internal_implementation.generate_mapping(create_tables =  True, check_tables = False)
        else:
            self.internal_implementation.generate_mapping(create_tables =  False, check_tables = False)

        # self.__session_factory = DBSessionContextManager(sql_debug =  self.is_debugging)

    @contextmanager
    def on_session(self) -> Any:
        with db_session:
            yield
        # yield self.__session_factory()

    @contextmanager
    def on_transactional_session(self) -> Any:
        with db_session:
            try:
                yield
                commit_session()
            except BaseException as e:
                # logging.exception("Got some exception")
                rollback_session()
                raise DyError(ErrorDefs.DB_OPERATE_FAILED.value, "Operate Database Failed", str(e)).as_exception()


@obj_d(OrmDef.PONY_ORM.value)
class PonyDatabaseDeclarative(BaseDatabaseDeclarative):
    def __init__(self, code_name:str):
        BaseDatabaseDeclarative.__init__(self, code_name)
        self.__database_implementation = DatabaseImplementation()

    @property
    def table(self) -> Any:
        return self.__database_implementation.Entity

    @property
    def internal_implementation(self) -> Any:
        return self.__database_implementation

    def make_proxy(self, **configuration:Any) -> IDatabaseProxy:
        return PonyDatabaseProxy(self.code_name, self, **configuration)