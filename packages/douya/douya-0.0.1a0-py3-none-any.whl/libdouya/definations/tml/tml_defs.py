# -*- coding:utf-8 -*-
#!/usr/bin/env python

"""
    tml_defs.py - 文件标记语言定义
"""

from enum import Enum,unique

@unique
class TmlDefs(Enum):
    JSON = "json"
    TOML = "toml"
    YAML = "yml:yaml"