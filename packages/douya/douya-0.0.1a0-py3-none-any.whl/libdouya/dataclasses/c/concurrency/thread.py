# -*- coding:utf-8 -*-
#!/usr/bin/env python

import threading,asyncio,logging
from typing import Callable
from .sleeper import Sleeper

class OnceshotThread(object):
    def __init__(self, name:str, callable:Callable, *args, **kwargs):
        self.__loop = asyncio.new_event_loop()
        self.__thread = threading.Thread(target = self.__loop.run_until_complete, name = name, args = (callable(*args, **kwargs), ))

    def spawn(self):
        self.__thread.start()

    def join(self):
        self.__thread.join()
        self.__loop.close()

class CirculativeThread(object):
    def __init__(self, name:str, callable:Callable, *args, **kwargs):
        self.__is_running = True

        self.__sleeper = Sleeper()
        self.__interval =  0

        self.__thread = threading.Thread(target = self.run, name = name, args = (callable, *args), kwargs = kwargs)

    def get_interval(self)->int: return self.__interval
    def set_interval(self, interval:int): self.__interval = 0 if 0 > interval else interval
    interval = property(get_interval, set_interval, None, '延时时间')

    def run(self, callable:Callable, *args, **kwargs):
        loop = asyncio.new_event_loop()
        while self.__is_running:
            try:
                loop.run_until_complete(callable(*args, **kwargs))
            except:
                logging.exception("Got exception")
            finally:
                self.__sleeper.sleep(self.__interval)
        loop.close()

    def spawn(self):
        self.__thread.start()

    def close(self):
        if self.__is_running:
            self.__is_running = False
            self.__sleeper.wakeup()

    def join(self):
        try:
            self.__thread.join()
        except KeyboardInterrupt:
            self.close()