# -*- coding:utf-8 -*-
#!/usr/bin/env python

from abc import ABCMeta, abstractmethod, abstractproperty
from typing import List

class IDyError(metaclass = ABCMeta):
    @abstractproperty
    def id(self)->int:
        '''错误码唯一编号'''

    @abstractproperty
    def code(self)->str:
        '''错误码唯一编码'''

    @abstractproperty
    def title(self)->str:
        '''错误码标题'''

    @abstractproperty
    def prompt_message(self)->str:
        '''错误码提示消息'''

    @abstractproperty
    def error_message(self)->str:
        '''错误码事故消息'''

    @abstractproperty
    def is_successful(self)->bool:
        '''是否成功'''

    @abstractmethod
    def append(self, other_error_messages:str) -> 'IDyError':
        '''附加其他错误消息'''

    @abstractmethod
    def as_exception(self):
        '''抛异常'''