# -*- coding:utf-8 -*-
#!/usr/bin/env python

import threading
from typing import Any

class Sleeper(object):
    def __init__(self, result:Any = None):
        self.__event = threading.Event()
        self.__result = result

    def sleep(self, delay_seconds:int) -> Any:
        self.__event.wait(delay_seconds)
        return self.__result

    def wakeup(self):
        self.__event.set()