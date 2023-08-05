# -*- coding:utf-8 -*-
#!/usr/bin/env python


'''
    path_utility.py - 路径相关的通用方法集
'''
import os
from typing import List

class PathUtl:
    @staticmethod
    def to_unique(*path_strings:List[str]) -> List[str]:
        '''路径去重复
        注：该方法不会改变目录的先后顺序
        '''
        outputs = []
        for i in range(len(path_strings)):
            p = os.path.abspath(path_strings[i])
            p = p.replace('\\', '/')

            for j in range(len(outputs)):    
                p1 = os.path.abspath(outputs[j]).replace('\\', '/')

                #不能使用os.path.samefile, 未见不存在时会抛异常
                if p == p1:
                    break
            else:
                outputs.append(path_strings[i])
        return outputs

    @staticmethod
    def cov_to_posix_path(path_string:str) -> str:
        return path_string.replace("\\", '/')

    @staticmethod
    def cov_to_nt_path(path_string:str) -> str:
        return path_string.replace("/", '\\')

    @staticmethod
    def cov_to_os_path(path_string:str) -> str:
        return PathUtl.cov_to_nt_path(path_string) if 'nt' == os.name else PathUtl.cov_to_posix_path(path_string)

    @staticmethod
    def is_sub(parent_path_string:str, *child_path_strings:List[str]) -> bool:
        parent_posix_path_string = PathUtl.cov_to_posix_path(parent_path_string)

        for child_path_string in child_path_strings:
            posix_path_string = PathUtl.cov_to_posix_path(child_path_string)
            if not posix_path_string.startswith(parent_posix_path_string):
                return False

        return True

    @staticmethod
    def find_sub(parent_path_string:str, *child_path_strings:List[str]) -> bool:
        parent_posix_path_string = PathUtl.cov_to_posix_path(parent_path_string)

        sub_paths = []
        for child_path_string in child_path_strings:
            posix_path_string = PathUtl.cov_to_posix_path(child_path_string)
            if posix_path_string.startswith(parent_posix_path_string):
                sub_paths.append(child_path_string)

        return sub_paths