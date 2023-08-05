# -*- coding:utf-8 -*-
#!/usr/bin/env python

from ...i.err import IDyError

class DyException(Exception):
    def __init__(self, error:IDyError):
        Exception.__init__(self, str(error))
        self.__error = error

    def append(self, *other_error_messages:str):
        self.__error.append(*other_error_messages)
        return self

    @property
    def error(self):
        return self.__error