# -*- coding:utf-8 -*-
#!/usr/bin/env python

import asyncio, asyncio.exceptions, threading, logging
from ....dataclasses.i.srv import IDyService
from ....dataclasses.c.concurrency.sleeper import Sleeper
from .parent import ServiceBaseRunner

class ServiceThreadRunner(ServiceBaseRunner):
    def __init__(self, service: IDyService):
        ServiceBaseRunner.__init__(self, service, threading.Event())
        self.__loop: asyncio.BaseEventLoop = asyncio.new_event_loop()
        self.__cron_sleeper: Sleeper = Sleeper()

    def run(self):
        try:
            # with __pypy__.thread.signals_enabled:

            # signames = ('SIGINT', 'SIGTERM', 'SIGQUIT') if 'nt' != os.name else ('CTRL_C_EVENT')
            # for signame in signames:
            #     loop.add_signal_handler(getattr(signal,signame), functools.partial(self.__terminate_service_gracefully, loop))
            for task in self.walk_service(self.__cron_sleeper):
                self.__loop.run_until_complete(task)
        except (KeyboardInterrupt, asyncio.exceptions.CancelledError):
            pass
        except BaseException as e:
            logging.exception(f"Got '{self.service.code}' service exception")
        finally:
            try:
                for task in asyncio.all_tasks():
                    if task.done(): continue
                    if task.cancel(): continue
                    logging.warn(f"Cancel task '{task.get_name()}' failed")
            finally:
                self.__loop.close()

    def before_halt(self):
        # super(DyThreadExecutiveService, self).halt_soon()
        if self.__cron_sleeper:
            self.__cron_sleeper.wakeup()

        if self.__loop and not self.__loop.is_closed():
            self.__loop.call_soon_threadsafe(self.__loop.stop)
