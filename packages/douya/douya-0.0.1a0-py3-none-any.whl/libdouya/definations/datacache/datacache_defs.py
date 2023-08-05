# -*- coding:utf-8 -*-
#!/usr/bin/env python

'''
    datacache_defs.py - 数据缓存相关
'''

from enum import Enum,unique

@unique
class DatacacheIdDef(Enum):
    ERROR = "error"