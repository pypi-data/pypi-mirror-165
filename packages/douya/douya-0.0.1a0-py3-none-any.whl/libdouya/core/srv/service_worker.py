# -*- coding:utf-8 -*-
#!/usr/bin/env python

import threading, multiprocessing, dataclasses
from typing import Union
from .runner import ServiceBaseRunner

@dataclasses.dataclass
class ServiceWorker:
    name: str
    runner: ServiceBaseRunner
    driver: Union[threading.Thread, multiprocessing.Process]