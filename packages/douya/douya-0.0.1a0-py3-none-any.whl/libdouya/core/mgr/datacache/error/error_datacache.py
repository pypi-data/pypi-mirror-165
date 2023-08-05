# -*- coding:utf-8 -*-
#!/usr/bin/env python

import typing, logging
from .....definations.datacache import DatacacheIdDef
from .....definations.err import ErrorDefs
from .....dataclasses.i.datacache import IDatacache, IDatacacheObjectBuilder
from .....dataclasses.c.err import DyError
from .....utilities.tml import TmlUtl
from ....mgr import ConfigurationMgr

class ErrorDatacacheObjectBuilder(IDatacacheObjectBuilder):
    def __init__(self, error_id:int, error_entry : typing.Dict[str, typing.Any]):
        IDatacacheObjectBuilder.__init__(self)
        self.__error_id = error_id
        self.__error_entry = error_entry
        self.__other_error_messages = []
        self.__keyword_argument = {}

    def and_other_error_messages(self, other_error_messages: typing.List[str]):
        self.__other_error_messages.extend(other_error_messages)
        return self

    def and_keyword_argument(self, keyword_argument: typing.Dict[str, typing.Any]):
        self.__keyword_argument.update(keyword_argument)
        return self
    
    def build(self) -> DyError:
        dy_error =  DyError(
            self.__error_id, 
            self.__error_entry.get("title"), 
            self.__error_entry.get("error_message"), 
            self.__error_entry.get("prompt_message"), 
            **self.__keyword_argument
        )
        if  self.__other_error_messages:
            dy_error.append(* self.__other_error_messages)

        return dy_error

class ErrorDatacache(IDatacache):
    def __init__(self):
        IDatacache.__init__(self)
        self.__default_language = None
        self.__error_entries = {}

    @property
    def id(self) -> str: return DatacacheIdDef.ERROR

    def intialize(self):
        try:
            for error_data_file in  ConfigurationMgr.get_instance().walk_appenv_files("errcfg.toml"):
                err_configuration = TmlUtl.load(error_data_file)
                logging.debug(f"Load error configuration: {err_configuration}")

                self.__default_language = err_configuration.get("default", {}).get("lan")
                for entry in err_configuration.get("entries", []):
                    if not entry: continue
                    for k, v in entry.items():
                        self.__error_entries.update({ k : v })
        except:
            logging.exception("Got an exception")

    def make_builder(self, id: typing.Union[int, ErrorDefs]) -> ErrorDatacacheObjectBuilder:
        error_id = int(id.value if isinstance(id, ErrorDefs) else id)
        is_successful = ErrorDefs.SUCCESS.value == error_id

        lan_entry = self.__error_entries.get(str(error_id))
        if not lan_entry:
            if substitute_lan_entry := self.__error_entries.get(str(ErrorDefs.SUCCESS.value if is_successful else ErrorDefs.FAILED.value)):
                lan_entry = substitute_lan_entry
            # else:
            #     lan_entry = {}

        entry = lan_entry.get(self.__default_language or "en")
        if not entry:
            entry.setdefault("title", "SUCCESS" if is_successful else "FAILED")
            entry.setdefault("error_message", "SUCCESS" if is_successful else "FAILED")
            entry.setdefault("prompt_message", "SUCCESS" if is_successful else "FAILED")

        return ErrorDatacacheObjectBuilder(error_id, entry)