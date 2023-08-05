# -*- coding:utf-8 -*-
#!/usr/bin/env python

"""
    dy_error.py - 错误的传递类
"""

from typing import Any
from ....definations.err import ErrorDefs
from ...i.err import IDyError
from .exception import DyException

class DyError(IDyError):
    def __init__(self, id:int, title:str, error_message:str, prompt_message:str = None, **keyword_argument:Any):
        self.__id = id
        self.__title = title
        self.__error_messages = [error_message]
        self.__prompt_messages = [prompt_message or error_message]
        self.__keyword_argument = keyword_argument

    def __repr__(self) -> str:
        return f'Errorcode(id={self.__id}, title={self.__title}, error_messages={self.__error_messages}, prompt_messages={self.__prompt_messages}, keyword_argument={self.__keyword_argument})'

    def __str__(self) -> str:
        return "[0x%x] %s - %s - %s" % (self.id, self.title, self.error_message, self.__get_keyword_string())

    def __add__(self, other_error_message) -> 'DyError':
        return self.append(other_error_message)

    def __get_keyword_string(self) -> str:
        return ' : '.join([f'{k} => {v}' for k, v in self.__keyword_argument.items()])

    @property
    def id(self)->int: return self.__id

    @property
    def code(self)->str: return "0x%x"%(self.__id)

    @property
    def title(self)->str: return self.__title or ""

    @property
    def prompt_message(self)->str:
        return '. '.join([ m.format(**self.__keyword_argument) for m in self.__prompt_messages if m ])

    @property
    def error_message(self)->str:
        return '. '.join([ m.format(**self.__keyword_argument) for m in self.__error_messages if m ])

    @property
    def is_successful(self) -> bool:
        return 0 == self.__id

    def append(self, *other_error_messages:str) -> 'DyError':
        if other_error_messages:
            for other_error_message in other_error_messages:
                if isinstance(other_error_message, IDyError):
                    self.__error_messages.append(other_error_message.error_message)
                    self.__prompt_messages.append(other_error_message.__prompt_messages)
                else:
                    self.__error_messages.append(str(other_error_message))
                    self.__prompt_messages.append(str(other_error_message))
        return self

    def as_exception(self):
        return DyException(self)
