# -*- coding:utf-8 -*-
#!/usr/bin/env python

import logging
from typing import Any, List, Iterable
from attrbox import AttrDict
from ...definations.cfg import DY_CONFIGURATION_KEY_DEF, ConfigerDefs
from ...dataclasses.i.srv import IDyService
from ...dataclasses.c.cfg import ServiceConfiger
from ...dataclasses.c.srv import BaseAsyncService
from ...dataclasses.c.db import Databases
from ...core.deco import configer_d
from ...core.mgr import NamingMgr

@configer_d(DY_CONFIGURATION_KEY_DEF.SERVICE, ConfigerDefs.SRV.value)
class DefaultServiceConfiger(ServiceConfiger):
    def __init__(self):
        ServiceConfiger.__init__(self)

    # def __enter__(self):
    #     return self

    # def __exit__(self,exc_type, exc_val, exc_tb):
    #     pass

    def group_services(self, dbs: Databases) -> Iterable[List[IDyService]]:
        srvs = []
        for service_code, service_configuration in self.configuration.items():
            try:
                logging.debug(f"The outter configuration of '{service_code}' service: {service_configuration}")

                #不启用
                if not service_configuration or service_configuration.get("disable"): continue

                srv: IDyService = NamingMgr.get_instance().new_naming(service_code)
                if not isinstance(srv, IDyService):
                    raise RuntimeError(f"Invalid service type: {service_code}")

                srv.code = service_code
                srv.databases = dbs
                srv.configuration = service_configuration.copy()
                logging.debug(f"The final configuration of '{service_code}' service: {srv.configuration}")

                srvs.append(srv)
            except:
                logging.exception(f"Got exception")

        yield [srvs]