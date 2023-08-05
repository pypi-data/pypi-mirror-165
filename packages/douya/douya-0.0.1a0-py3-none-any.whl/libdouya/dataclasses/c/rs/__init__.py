# -*- coding:utf-8 -*-
#!/usr/bin/env python

from typing import Any,Dict,List
from dataclasses import dataclass, field, asdict
from ....definations.err import ErrorDefs
from ..err import DyError
from .metadata import Metadata
from .pagination import Pagination
from .statusdata import Statusdata

@dataclass
class Req(object):
    version: str = "v1"
    metadata: Metadata = None
    data: Dict[str,Any] = field(default_factory = dict)

    def to_dict(self):
        return asdict(self)

    @staticmethod
    def from_dict(data:Dict[str, Any]):
        if not data: return None
        return Req(
            version = data.get('version'),
            metadata = Metadata.from_dict(data.get('metadata')),
            data = data.get('data')
        )

    @staticmethod
    def build(data:Any, version:str = "v1", metadata:Metadata = None) -> 'Req':
        return Req(
            version = version,
            metadata = metadata,
            data = data
        )

@dataclass
class Res(object):
    version: str = "v1"
    statusdata: Statusdata = None
    metadata: Metadata = None
    datas: List[Any] = field(default_factory=list)

    def to_dict(self):
        return asdict(self)

    @staticmethod
    def from_dict(data:Dict[str, Any]):
        if not data: return None
        return Res(
            version = data.get('version'),
            statusdata = Statusdata.from_dict(dict.get('statusdata')),
            metadata = Metadata.from_dict(dict.get('metadata')),
            datas = data.get('datas') or []
        )

    def copy_metadata(self, metadata:Metadata = None):
        if metadata:
            self.metadata = metadata

    def is_ok(self) -> bool:
        return self.statusdata and ErrorDefs.SUCCESS.value == self.statusdata.id

    @staticmethod
    def success(*datas):
        return Res (
            version = "v1",
            statusdata = Statusdata(
                id = 0,
                prompt_message = "",
                message = ""
            ),
            datas = datas
        )

    @staticmethod
    def fail(err: DyError,  *datas):
        return Res (
            version = "v1",
            statusdata = Statusdata(
                id = err.id,
                prompt_message = err.prompt_message,
                message = str(err)
            ),
            datas = datas
        )


__all__ = [
    "Metadata",
    "Pagination",
    "Statusdata",
    "Req", "Res"
]
