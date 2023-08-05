# -*- coding:utf-8 -*-
#!/usr/bin/env python

from dataclasses import dataclass
from typing import Any,Dict
from ....definations.err import ErrorDefs
# from ..c.err import DyError
from .pagination import Pagination

@dataclass
class Metadata(object):
    seq: str = None
    pagination: Pagination = None
    passback: Dict[str, Any] = None
    forwared_for: str = None
    track_service_url: str = None

    @staticmethod
    def from_dict(data:Dict[str, Any]):
        if not data: return None

        return Metadata(
            seq = data.get('seq'),
            pagination = Pagination.from_dict(data.get('pagination')),
            passback = data.get('passback'),
            forwared_for = data.get('forwared_for'),
            track_service_url = data.get('track_service_url')
        )
        
