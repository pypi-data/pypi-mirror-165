# -*- coding:utf-8 -*-
#!/usr/bin/env python

from dataclasses import dataclass
from typing import Dict, Any
from ....definations.err import ErrorDefs
from ..err import DyError

@dataclass
class Pagination:
    offset: int
    limit: int
    total: int

    @staticmethod
    def from_dict(data:Dict[str, Any]):
        if not data: return None
        return Pagination(
            offset = data.get('offset'),
            limit = data.get('limit'),
            total = data.get('total')
        )

    @staticmethod
    def from_page(page_number:int, page_size:int, total_size:int = -1) -> 'Pagination':
        if 0 >= page_number: raise DyError(ErrorDefs.ARG_VALIDATION_FAILED.value, page_number = page_number).exception()
        if 0 > page_size: raise DyError(ErrorDefs.ARG_VALIDATION_FAILED.value, page_size = page_size).exception()
        if -1 > total_size: total_size = -1
        return Pagination(offset = (page_number - 1) * page_size, limit =  page_size, total_size = total_size)