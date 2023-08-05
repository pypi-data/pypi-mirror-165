# -*- coding:utf-8 -*-
#!/usr/bin/env python

import enum

@enum.unique
class DyUrlDefs(enum.Enum):
    CONF = 'conf'

    def yes(self, url_str:str) -> bool:
        return url_str.startswith(f'{self.value}://')