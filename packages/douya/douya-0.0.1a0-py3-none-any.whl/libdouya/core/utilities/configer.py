# -*- coding:utf-8 -*-
#!/usr/bin/env python

import urllib.parse
from ...definations import DyUrlDefs

def make_configer_url(key:str) -> str:
    path = key.replace(".", "/")
    return f'{DyUrlDefs.CONF.value}:///{path}'

def parse_configer_key_by_url(url:str) -> str:
    u = urllib.parse.urlparse(url)
    key = u.path[1:].replace('/', '.')
    return key