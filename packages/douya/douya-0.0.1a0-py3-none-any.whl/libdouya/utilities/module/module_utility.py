# -*- coding:utf-8 -*-
#!/usr/bin/env python

"""
    module_utility.py - 包相关功能函数
"""

import logging, inspect, pkgutil, typing, importlib.util

class ModuleUtl:
    @staticmethod
    def is_module(o):
        return inspect.ismodule(o)

    @staticmethod
    def is_imported(self, module_name:str):
        spec = importlib.util.find_spec(module_name)
        return True if spec else False

    # def import_thing(self, module_name, name):
    #     module = importlib.import_module(module_name)
    #     return getattr(module, name)

    @staticmethod
    def get_module_info(func_or_method_or_type: typing.Any):
        return inspect.getmodule(func_or_method_or_type).__name__, func_or_method_or_type.__name__

    @staticmethod
    def import_submodule_recursively(module: typing.Any, is_pkg_useable:bool = None):
        submodules = dict()

        if is_pkg_useable:
            is_pkg_useable = False

        for loader, submodule_name, is_pkg in pkgutil.walk_packages(module.__path__, module.__name__ + "."):
            try:
                if is_pkg_useable or not is_pkg:
                    submodule = loader.find_module(submodule_name).load_module(submodule_name)
                    submodules.update({ submodule_name : submodule })
            except BaseException as ex:
                logging.exception(f"Got exception when load this module of '{submodule_name}'")
            # for name in dir(module):
            #     obj = getattr(module, name)
            #     if isinstance(obj, type) and issubclass(obj, unittest.case.TestCase):
            #         exec ('%s = obj' % obj.__name__)
        return submodules

    @staticmethod
    def import_module(*module_names: str, **kwargs: typing.Any):
        modules = dict()

        if not module_names:
            return []
        
        for module_name in module_names:
            try:
                m = importlib.import_module(module_name, **kwargs)
                modules.update({ module_name : m})
            except BaseException as ex:
                logging.exception(f"Got exception when load this module of '{module_name}'")
        return modules

    @staticmethod
    def import_module_recursively(*module_names: str):
        if not module_names:
            return []

        for name, module in ModuleUtl.import_module(*module_names).items():
            logging.info(f"Import modules: {name}")
            submodules = ModuleUtl.import_submodule_recursively(module)
            logging.info(f"Import submodules: {','.join(submodules.keys())}")

    @staticmethod
    def scan_module(module_name:str , is_recursive:bool = None):
        if not is_recursive:
            is_recursive = False

        for name,module in ModuleUtl.import_module(module_name).items():
            #当前模块
            yield module

            #子模块
            if not is_recursive: continue
            for loader, submodule_name, is_pkg in pkgutil.walk_packages(module.__path__, module.__name__ + '.'):
                yield loader.find_module(submodule_name).load_module(submodule_name)