# -*- coding:utf-8 -*-
#!/usr/bin/env python

import logging, threading, multiprocessing
from typing import Iterable, Iterable
# from ...dataclasses.i.svc.service import IDyServer
from ...dataclasses.i.srv import IDyService
from .runner import ServiceThreadRunner, ServiceProcessRunner
from .service_worker import ServiceWorker

class ServiceTask(object):
    def __init__(self,  *services: IDyService):
        self.__services = services

    def __stop_workers(self, *workers: ServiceWorker):
        #pthread_kill
        for worker in workers:
            try:
                worker.runner.before_halt()
            except:
                logging.exception(f"Got an exception when halt {worker.name} before ")
            try:
                worker.runner.signal_to_halt()
            except:
                logging.exception(f"Got an exception when signal {worker.name} to halt")

        for worker in workers:
            try:
                if worker.driver.is_alive():
                    worker.driver.join()
            except:
                logging.exception(f"Got an exception when wait {worker.name} stopped")

            try:
                if not worker.driver.is_alive() and isinstance(worker.driver, multiprocessing.Process):
                    worker.driver.kill()
                worker.runner.after_halt()
            except:
                logging.exception(f"Got an exception when kill {worker.name}")

    def __create_workers(self) -> Iterable[ServiceWorker]:
        for srv in self.__services:
            parallel_number = srv.parallel_number or 1
            for i in range(parallel_number):
                if srv.parallel_mode == 'mp':
                    runner = ServiceProcessRunner(srv)
                    p = multiprocessing.Process(target = ServiceProcessRunner.run, name = srv.code, args = (runner, ))
                    p.start()
                    yield ServiceWorker(name = f"{srv.code}-{i}", runner = runner, driver = p)
                else:
                    runner = ServiceThreadRunner(srv)
                    t = threading.Thread(target = runner.run, name = srv.code, daemon = True)
                    t.start()
                    yield ServiceWorker(name = f"{srv.code}-{i}",  runner = runner, driver = t)

    def __await__(self):
        # def signal_handler(signum, frame):
        #     print("1"*30)
        #     self.__exiting_flag.set()
        # signal.signal(signal.SIGTERM, functools.partial(lambda flag: flag.set(), self.__exiting_flag))
        #程序结束信号
        # signal.signal(signal.SIGTERM, signal_handler)
        #监听LINUX的程序打断(interrupt)信号，通是CTLR-C
        # signal.signal(signal.SIGINT, signal_handler)

        # try:
        #     # event = threading.Event(1)
        #     # help(signal)
        #     signal.pause()
        #     # signal.set_wakeup_fd(-1)
        # except (KeyboardInterrupt, CancelledError):
        #     pass

        # 将多线程和多进程的服务进行分组
        workers = []
        try:
            for worker in self.__create_workers():
                logging.info(f"Schedule task: {worker.name}")
                workers.append(worker)
        except:
            logging.exception("Got an exception")

        try:
            while any([ worker.driver.is_alive() for worker in workers]):
                yield

            # for future in concurrent.futures.as_completed(futures_buffer):
            #     try:
            #         res = future.result()
            #     except (KeyboardInterrupt, CancelledError):
            #         print('1'*30)
            #         if mp_pool:
            #             for pid in mp_pool._processes:
            #                 os.kill(pid, signal.SIGKILL)
            #         if mt_pool:
            #             mt_pool.shutdown(wait = True)
            #     except Exception:
            #         logging.exception("Got exception")
        except (KeyboardInterrupt, ): 
            pass
        except ValueError:
            pass
        finally:
            self.__stop_workers(*workers)
            logging.info("Exit task")