# -*- coding:utf-8 -*-
#!/usr/bin/env python

from dataclasses import dataclass
from typing import Dict, Any

@dataclass
class Statusdata(object):
    id: int
    prompt_message: str = None
    message: str = None

    @staticmethod
    def from_dict(data:Dict[str, Any]):
        if not data: return None

        return Statusdata(
            id = data.get('id'),
            prompt_message = data.get('prompt_message'),
            message = data.get('message')
        )