
# -*- coding:utf-8 -*-
#!/usr/bin/env python

from typing import Any

def is_integer(value: Any) -> bool:
    return isinstance(value, int)

def is_port(value:Any) -> bool:
    return is_integer(value) and 0 < value and 65536 > value