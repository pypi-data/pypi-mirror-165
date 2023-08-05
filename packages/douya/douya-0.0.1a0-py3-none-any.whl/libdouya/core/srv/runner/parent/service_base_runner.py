# -*- coding:utf-8 -*-
#!/usr/bin/env python

import logging, threading, multiprocessing, datetime
from typing import Union
from abc import ABCMeta, abstractmethod
from croniter import croniter
from .....definations.cfg import ConfigerDefs
from .....dataclasses.i.srv import IDyService
from .....dataclasses.c.concurrency.sleeper import Sleeper
from ....mgr import ConfigurationMgr

class ServiceBaseRunner(metaclass = ABCMeta):
    def __init__(self, service: IDyService, halt_flag: Union[threading.Event, multiprocessing.Event]):
        self.__service = service
        self.__halt_flag = halt_flag

    def get_service(self) -> IDyService: return self.__service
    service = property(get_service, None, None, '服务')

    def is_running(self) -> bool:
        '''是否运行
        '''
        return not self.__halt_flag.is_set()

    @abstractmethod
    def run(self): pass

    def before_halt(self): pass

    def after_halt(self): pass

    def signal_to_halt(self):
        self.__halt_flag.clear()
        self.__halt_flag.set()

    def walk_service(self, cron_sleeper: Sleeper):
        if self.service.databases:
            with ConfigurationMgr.get_instance().get_configer(ConfigerDefs.DB.value) as cf:
                cf.establish_connection(self.service.databases)

        # if t1 is not None and 0 == getattr(t1 - t0, 'seconds'):
        #     t0 = t0 + datetime.timedelta(seconds = 1)
        logging.info(f"The '{self.service.code}' service is initializing.")
        yield self.service.initialize()
        logging.info(f"The '{self.service.code}' service is initialized.")

        logging.info(f"The '{self.service.code}' service is serving.")
        cron_expression = self.service.schedule_configuration and self.service.schedule_configuration.get("cron")

        if cron_expression:
            iter = croniter(cron_expression)
            while self.is_running():
                # t0 = time.time()
                # t1 = iter.get_next(float, t0)
                # t = t1 - t0
                # logging.debug(f"Sleep  {t} seconds")
                # cron_sleeper.sleep(t)
                t0 = datetime.datetime.now()
                t1 = iter.get_next(datetime.datetime, t0)
                delta = t1 - t0
                cron_sleeper.sleep(delta.total_seconds())
                logging.debug(f"Sleep  {delta.total_seconds()} seconds")

                # loop.run_until_complete(asyncio.sleep(getattr(t1 - t0, 'seconds')))
                yield self.service.serve()
        else:
            yield self.service.serve()
        logging.info(f"The '{self.service.code}' service is served.")