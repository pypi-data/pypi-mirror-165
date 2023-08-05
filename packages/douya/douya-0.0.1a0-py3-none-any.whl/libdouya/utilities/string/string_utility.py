# -*- coding:utf-8 -*-
#!/usr/bin/env python

'''
    string_utility.py - 字符串相关的通用方法集
'''

import re, uuid
from typing import Any

class StrUtl(object):
    @staticmethod
    def cast_to(obj_str:str, obj_type:str, **kwargs) -> Any:
        if 'string' == obj_type:
            return obj_str
        elif 'integer' == obj_type:
            return int(obj_type, **kwargs)
        elif obj_type in ['float', 'double']:
            return float(obj_type, **kwargs)
        pass

    @staticmethod
    def cov_to_first_char_uppercase(src_str:str) -> str:
        return src_str[0:1].upper() + src_str[1:]

    @staticmethod
    def cov_camel_to_snake(camel_str:str) -> str:
        '''驼峰形式字符串转成下划线形式
        :param hunp_str: 驼峰形式字符串
        :return: 字母全小写的下划线形式字符串
        '''
        # 匹配正则，匹配小写字母和大写字母的分界位置
        p = re.compile(r'([a-z]|\d)([A-Z])')
        # 这里第二个参数使用了正则分组的后向引用
        sub = re.sub(p, r'\1_\2', camel_str).lower()
        return sub

    @staticmethod
    def cov_camel_to_dot(camel_str:str):
        '''驼峰形式字符串转成逗号形式
        :param camel_str: 驼峰形式字符串
        :return: 字母全小写的下划线形式字符串
        '''
        # 匹配正则，匹配小写字母和大写字母的分界位置
        p = re.compile(r'([a-z]|\d)([A-Z])')
        # 这里第二个参数使用了正则分组的后向引用
        sub = re.sub(p, r'\1.\2', camel_str).lower()
        return sub

    @staticmethod
    def cov_snake_to_camel(snake_case_str:str, is_startswith_uppercase = False):
        '''下划线形式字符串转成驼峰形式
        :param snake_case_str: 下划线形式字符串
        :return: 驼峰形式字符串
        '''
        # 这里re.sub()函数第二个替换参数用到了一个匿名回调函数，回调函数的参数x为一个匹配对象，返回值为一个处理后的字符串
        sub = re.sub(r'(_\w)',lambda x:x.group(1)[1].upper(),snake_case_str)
        return sub if not is_startswith_uppercase else StrUtl.cov_to_first_char_uppercase(sub)

    @staticmethod
    def cov_snake_to_dot(snake_case_str:str):
        '''下划线形式字符串转成逗号形式
        :param snake_case_str: 下划线形式字符串
        :return: 逗号形式字符串
        '''
        # 这里re.sub()函数第二个替换参数用到了一个匿名回调函数，回调函数的参数x为一个匹配对象，返回值为一个处理后的字符串
        sub = re.sub(r'(_)', ".", snake_case_str)
        return sub

    @staticmethod
    def cov_encoding(input_str:str, source_encoding_str:str, dest_encoding_str:str):
        # return source_str.encode(source_encoding_str, 'ignore').decode(dest_encoding_str, 'ignore')
        # print(source_str.encode(dest_encoding_str, 'ignore'))
        return input_str.encode(source_encoding_str).decode(dest_encoding_str)

    @staticmethod
    def gen_uuid(name:str = None):
        if name:
            return uuid.uuid3(uuid.NAMESPACE_DNS, name).hex
        else:
            return uuid.uuid1().hex