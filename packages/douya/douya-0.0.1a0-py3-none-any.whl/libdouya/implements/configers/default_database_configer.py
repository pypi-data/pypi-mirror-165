# -*- coding:utf-8 -*-
#!/usr/bin/env python

import logging
from typing import List,Dict,Any#,Union
from attrbox import AttrDict

# from libdouya.core.mgr.naming_mgr.naming_mgr import NamingMgr
from ...definations.cfg import DY_CONFIGURATION_KEY_DEF, ConfigerDefs
from ...dataclasses.i.rdb import IDatabaseDeclarative, IDatabases
from ...dataclasses.c.cfg import DatabaseConfiger
from ...dataclasses.c.db import Databases
from ...core.deco import configer_d

@configer_d(DY_CONFIGURATION_KEY_DEF.DATABASE, ConfigerDefs.DB.value)
class DefaultDatabaseConfiger(DatabaseConfiger):
    def __init__(self):
        DatabaseConfiger.__init__(self)

    def establish_connection(self, databases: IDatabases):
        for code_name in databases.code_names:
            databases.db(code_name).establish_connection()

    def initialize_and_get_databases(self, *declaratives:IDatabaseDeclarative) -> IDatabases:
        dbs = []
        for declarative in declaratives:
            subcfg = self.configuration.get(declarative.code_name)
            if not subcfg or subcfg.get("disable"): return

            db = declarative.make_proxy(**subcfg)

            try:
                db.initialize()
                dbs.append(db)
            except:
                logging.exception(f"Initialize database failed: {db.code_name}")

        return Databases(*dbs)