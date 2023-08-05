# -*- coding:utf-8 -*-
#!/usr/bin/env python

import asyncio, asyncio.exceptions, multiprocessing, os, signal, logging, functools, time
from ....dataclasses.i.srv import IDyService
from ....dataclasses.c.concurrency.sleeper import Sleeper
from .parent import ServiceBaseRunner

class ServiceProcessRunner(ServiceBaseRunner):
    def __init__(self, service: IDyService):
        ServiceBaseRunner.__init__(self, service, multiprocessing.Event())

    @staticmethod
    def cancel_all_task(loop: asyncio.BaseEventLoop, cron_sleeper: Sleeper):
        if not cron_sleeper:
            cron_sleeper.set()

        if tasks := [ task for task in asyncio.all_tasks(loop) if not task.done() ]:
            for task in tasks:
                if not task.cancel():
                    logging.warn(f"Cancel task '{task.get_name()}' failed")

    def run(self):
        loop = asyncio.new_event_loop()
        sleeper = Sleeper()

        try:
            signames = ('SIGINT', 'SIGTERM', 'SIGQUIT') if 'nt' != os.name else ('CTRL_C_EVENT', 'SIGBREAK')
            for signame in signames:
                loop.add_signal_handler(getattr(signal,signame), functools.partial(self.cancel_all_task, loop, sleeper))

            for task in self.walk_service(sleeper):
                loop.run_until_complete(task)
        except (KeyboardInterrupt, asyncio.exceptions.CancelledError):
            pass
        except BaseException as e:
            logging.exception(f"Got '{self.service.code}' service exception")
        finally:
            loop.close()