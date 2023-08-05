# -*- coding:utf-8 -*-
#!/usr/bin/env python

'''
    db_defs.py - 数据库相关
'''

from enum import Enum,unique

@unique
class DialectDef(Enum):
    SQLITE = "sqlite"
    PG = "postgresql"

@unique
class OptDef(Enum):
    CREATING_TABLES = "creating_tables"
    DROPPING_TABLES = "dropping_tables"

@unique
class OrmDef(Enum):
    PONY_ORM = "orm:pony"
    SQLALCHEMY_ORM = "orm:sqlalchemy"

@unique
class OrmConnectionPoolTypeDef(Enum):
    EVERY_PROCESSOR = "mp"
    EVERY_THREAD = "mt"
    ONLY_ONE = "one"
