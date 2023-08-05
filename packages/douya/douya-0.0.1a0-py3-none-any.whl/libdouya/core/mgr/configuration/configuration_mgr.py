# -*- coding:utf-8 -*-
#!/usr/bin/env python

import os,logging,json
from functools import reduce
from typing import Union, List, Dict, Iterator, Any
from attrbox import AttrDict, dict_set, dict_get, dict_merge
from ....definations import DyUrlDefs
from ....definations.cfg import EnvDefs,EnvFilterModeDef,EnvSelectModeDef, DY_CONFIGURATION_KEY_DEF
from ....dataclasses.i.cfg import IBaseConfiger
from ....utilities.singleton import Singleton
from ....utilities import StrUtl, PathUtl, TmlDefs, TmlUtl
from ...utilities.configer import parse_configer_key_by_url
from ..naming import NamingMgr
from .constant import CONFIGURATION_DFLT_DEF, ENVIRONMENT_MAPPING_CONFIGURATION_DFLT_DEF
# from .db import DatabaseConfigurer

class EnvironmentConfiguration(object):
    '''环境变量的配置管理
    '''
    def __init__(self):
        # << json.load(open('test/example-appengine.json'))
        self.__env_mapping_info = {}
        # self.__env_mapping_info = TmlUtl.loads_attr(env_mapping_cfg_str, TmlDefs.TOML)

    def merge_configuration(self, *env_cfg_strs:List[str]):
        for env_mapping_cfg_str in env_cfg_strs:
            try:
                cnf = TmlUtl.loads_attr(env_mapping_cfg_str, TmlDefs.TOML) or {}
                dict_merge(self.__env_mapping_info, *[ { k : c } for c in cnf.get("envs", []) if (k := c.get("name")) ])
            except:
                logging.exception(f"Load environment configuration failed: {env_mapping_cfg_str}")

    def write_to(self, configuration: AttrDict):
        for env_cfg in self.__env_mapping_info.values():
            name = env_cfg.get('name')
            if not name: continue

            paths = env_cfg.get("paths")
            if not paths: continue

            for p in paths:
                try:
                    if v := self.get_env(name):
                        dict_set(configuration, p, v)
                except BaseException:
                    logging.exception("Invalid exception")

    def get_env(self, env_name:str, default_value:Any = None) -> Any:
        env_value = os.environ.get(env_name, default_value)
        if (env_cfg := self.__env_mapping_info.get(env_name)) and env_value:
            return StrUtl.cast_to(env_cfg.get("format", "%s") % (env_value), env_cfg.get("type", "string"))
        else:
            return env_value

    @property
    def appenv(self) -> Union[str, None]:
        return self.get_env(EnvDefs.APP_ENV.name)

    @property
    def work_directory(self) -> str:
        return self.get_env(EnvDefs.APP_WORK_DIR.name, ".")

    @property
    def configuration_directories(self) -> List[str]:
        val_str = self.get_env(EnvDefs.APP_CFG_DIR.name, ".:config")
        if not val_str:
            raise RuntimeError(f"Miss the '{EnvDefs.APP_CFG_DIR.name}' configuration")
        dirs = list(map(os.path.abspath, val_str.split(":")))
        return PathUtl.to_unique(*dirs)

    @property
    def configuration_names(self) -> List[str]:
        val_str = self.get_env(EnvDefs.APP_CFG_NAME.name, "app.toml:app.json")
        if not val_str:
            raise RuntimeError(f"Miss the '{EnvDefs.APP_CFG_NAME.name}' configuration")
        return reduce(lambda x, y: y if y in x else x+[y], [[], ] + val_str.split(":"))

    @property
    def lookup_directories(self):
        val_str = self.get_env(EnvDefs.APP_LOOKUP_DIR.name, ".")
        if not val_str:
            raise RuntimeError(f"Miss the '{EnvDefs.APP_LOOKUP_DIR.name}' configuration")

        dirs = []
        dirs.extend(self.configuration_directories)
        dirs.extend(map(os.path.abspath, val_str.split(":")))
        return PathUtl.to_unique(*dirs)

class ConfigurationMgr(metaclass = Singleton):
    def __init__(self):
        self.__app_env = None
        self.__env_cfg = None
        self.__configuration = None

    # def __parse_configuration_file(self, configuration_file_path):
    #     return None

    def __get_app_env_file_names(self, path_str:str, contains_other_markup_language_file = False) -> List[str]:
        '''获得环境文件的名字
        contains_other_markup_language_file {bool} 是否包含其他标记语言文件。
                                                   启用该项以后，会返回同名的其他的环境文件。例如：app.yaml匹配的环境文件app-dev.json、app-dev.yaml和app-dev.toml等。
                                                   若不开启，返回的环境扩展名，必需和输入的文件扩展名一致。例如：app.csv匹配的环境文件app-dev.csv。
        '''
        if not self.__app_env: return None

        lan = TmlUtl.guess_file(path_str)
        filename,extname = os.path.splitext(os.path.basename(path_str))

        file_names = []
        if lan and contains_other_markup_language_file:
            file_names.extend(TmlUtl.suffix_extend_names(f"{filename}-{self.__app_env}", *TmlDefs.__members__.values()))
        else:
            file_names.append(f'{filename}-{self.__app_env}{extname}')

        return file_names

    def __walk_app_env_files_with_same_directory(self, path_str:str, contains_other_markup_language_file:bool = False):
        '''扫描当前目录的环境文件。
        '''
        if not self.__app_env:
            return

        dirpath = os.path.dirname(path_str)
        if os.path.exists(dirpath):
            for app_env_file_name in self.__get_app_env_file_names(path_str,  contains_other_markup_language_file):
                p = os.path.join(dirpath, app_env_file_name)
                if os.path.exists(p):
                    yield p

    def __reload_environment_variables(self, *env_cfg_strs:List[str]):
        '''重建加载环境变量
        '''
        self.__env_cfg = EnvironmentConfiguration()
        self.__env_cfg.merge_configuration(ENVIRONMENT_MAPPING_CONFIGURATION_DFLT_DEF, *env_cfg_strs)

        workdir = self.__env_cfg.work_directory
        if not os.path.exists(workdir):
            raise RuntimeError(f"The work directory path doesn't exists - path({workdir})")

        if not os.path.samefile(workdir, "."):
            os.chdir(workdir)

    @staticmethod
    def get_instance() -> 'ConfigurationMgr':
        '''
        由于是单例，所以调用构造函数永远都返回同一个实例
        '''
        return ConfigurationMgr()

    def init(self, env = None, *env_cfg_strs:List[str]):
        self.__reload_environment_variables(*env_cfg_strs)

        self.__app_env = env if env else self.__env_cfg.appenv
        
        self.__configuration = TmlUtl.loads_attr(CONFIGURATION_DFLT_DEF, TmlDefs.TOML)

        for dp in self.__env_cfg.configuration_directories:
            for fp in self.__env_cfg.configuration_names:
                p = os.path.join(dp, fp)
                try:
                    self.load_configuration_file(p)
                except BaseException as e:
                    print(e)
                    logging.exception(f"Failed to load configuration file - path({p})")

        # 环境变量可以覆盖其他变量
        self.__env_cfg.write_to(self.__configuration)

        for catalog_dir in self.get_conf(DY_CONFIGURATION_KEY_DEF.CATALOG, {}).values():
            d = PathUtl.cov_to_os_path(catalog_dir)
            d = os.path.abspath(d)
            os.makedirs(d, exist_ok=True)

        logging.debug(f"The application configuration: {json.dumps(self.configuration)}")

    @property
    def configuration(self):
        '''
        获得配置信息
        '''
        return self.__configuration

    def get_conf(self, key_or_url:str, default_value:Any = None) -> AttrDict:
        if DyUrlDefs.CONF.yes(key_or_url):
            key = parse_configer_key_by_url(key_or_url)
        else:
            key = key_or_url

        if not key: return default_value

        v = dict_get(self.configuration, key)
        if v is None: return default_value

        return v

    def get_configer(self, name:str, *args:List[Any], **kwargs:Dict[str,Any]) -> Any:
        urls = NamingMgr.get_instance().get_alias_urls(name)
        if not urls: raise RuntimeError(f"Can't find configer: {name}")
        logging.info(f"Find configuration url: {urls}")

        cfg = self.get_conf(urls[-1])
        if cfg is None: raise RuntimeError(f"Can't find configuration: {urls[-1]}")

        c : IBaseConfiger = NamingMgr.get_instance().new_naming(name)
        if c is None: raise RuntimeError(f"Can't create configer: {name}")

        c.configuration = cfg
        c.initialize(*args, **kwargs)
        return c

    def try_to_get_configer(self, name:str, *args:List[Any], **kwargs:Dict[str,Any]) -> Any:
        try:
            return self.get_configer(name, *args, **kwargs)
        except BaseException as e:
            logging.warning(str(e))
            return None

    def merge_configuration(self, configuration:Dict[str,Any]):
        if not isinstance(configuration, Dict): return
        dict_merge(self.__configuration, configuration)

    def load_configuration_file(self, path_str: os.PathLike):
        '''
        读取配置文件
        '''
        ipaths = []
        
        # 读取配置文件并合并配置
        if os.path.exists(path_str):
            dict_merge(self.__configuration, TmlUtl.load(path_str, None))
            ipaths.append(path_str)

        for p in self.__walk_app_env_files_with_same_directory(path_str, True):
            dict_merge(self.__configuration, TmlUtl.load(p, None))
            ipaths.append(p)

        logging.info(f'Load configuration files: {":".join(ipaths)}')
        
        # 如果存在其他环境版本的配置文件，则读取，并合并

    def as_run_diretory(self, sub_path:os.PathLike = None) -> os.PathLike:
        p = self.get_conf(DY_CONFIGURATION_KEY_DEF.RUN_CATALOG_DIR)
        if p: p = PathUtl.cov_to_os_path(p)
        if sub_path: p = os.path.join(p, PathUtl.cov_to_os_path(sub_path))
        return os.path.abspath(p)

    def as_data_diretory(self, sub_path:os.PathLike = None) -> os.PathLike:
        p = self.get_conf(DY_CONFIGURATION_KEY_DEF.DATA_CATALOG_DIR)
        if p: p = PathUtl.cov_to_os_path(p)
        if sub_path: p = os.path.join(p, PathUtl.cov_to_os_path(sub_path))
        return os.path.abspath(p)

    def as_binary_diretory(self, sub_path:os.PathLike = None) -> os.PathLike:
        p = self.get_conf(DY_CONFIGURATION_KEY_DEF.BINARY_CATALOG_DIR)
        if p: p = PathUtl.cov_to_os_path(p)
        if sub_path: p = os.path.join(p, PathUtl.cov_to_os_path(sub_path))
        return os.path.abspath(p)

    def as_temporary_diretory(self, sub_path:os.PathLike = None) -> os.PathLike:
        p = self.get_conf(DY_CONFIGURATION_KEY_DEF.TEMPORARY_CATALOG_DIR)
        if p: p = PathUtl.cov_to_os_path(p)
        if sub_path: p = os.path.join(p, PathUtl.cov_to_os_path(sub_path))
        return os.path.abspath(p)

    def as_backup_diretory(self, sub_path:os.PathLike = None) -> os.PathLike:
        p = self.get_conf(DY_CONFIGURATION_KEY_DEF.BACKUP_CATALOG_DIR)
        if p: p = PathUtl.cov_to_os_path(p)
        if sub_path: p = os.path.join(p, PathUtl.cov_to_os_path(sub_path))
        return os.path.abspath(p)

    def walk_appenv_files(self, file_path: os.PathLike, *ext_dirs:List[os.PathLike], **parameter_info: Dict[str,Any]) -> Iterator[str]:
        '''工作目录扫描指定文件
        file_path {PathLike} 需要扫描的父目录
        ext_dirs {PathLike} 其他扫描目录
        filter_mode {EnvFilterModeDef} 过滤的方式
        select_mode {EnvSelectModeDef} 选出的方式
        walking_subdirs {bool} 是否扫描子目录
        containing_env_dirs {bool} 是否包括环境目录
        '''

        filter_mode:str = parameter_info.get('filter_mode', EnvFilterModeDef.ENV_FILES_FIRST.name)
        select_mode:str = parameter_info.get('select_mode', EnvSelectModeDef.ANY.name)
        walking_subdirs:bool = parameter_info.get('walking_subdirs', False)
        containing_env_dirs:bool = parameter_info.get('containing_env_dirs', False)

        dirs = [ d for d in self.__env_cfg.lookup_directories if d and os.path.exists(d) ]
        dirs.append(self.as_data_diretory())

        if containing_env_dirs:
            dirs.extend([ d for d in self.__env_cfg.configuration_directories if d and os.path.exists(d) ] )
        
        if ext_dirs:
            dirs.extend([ os.path.abspath(d) for d in ext_dirs if d and os.path.exists(d)])
        
        if walking_subdirs:
           for d in dirs:
               for root, subdirs, _ in os.walk(d):
                   dirs.extend([ os.path.join(root, sd) for sd in subdirs])

        dirs = PathUtl.to_unique(*dirs) 

        for d in dirs:
            # 定义变量
            p = file_path if os.path.isabs(file_path) else os.path.join(d, file_path)
            base_file,env_files,final_files = None, [], []

            # 检索当前目录下面的原名文件和环境文件
            if os.path.exists(p):
                base_file = p

            for env_file in self.__walk_app_env_files_with_same_directory(p):
                env_files.append(env_file)

            # 根据各种搜索模式，将有效的路径名，选入final_files
            if filter_mode == EnvFilterModeDef.EXINCLUDING_ENV_FILES.name:
                if base_file:
                    final_files.append(base_file)
            elif filter_mode == EnvFilterModeDef.ONLY_ENV_FILES.name:
                if env_files:
                    final_files.extend(env_files)
            elif filter_mode == EnvFilterModeDef.ENV_FILES_FIRST.name:
                if env_files:
                    final_files.extend(env_files)
                elif base_file:
                    final_files.append(base_file)
            elif filter_mode == EnvFilterModeDef.ALL.name:
                if base_file:
                    final_files.append(base_file)
                if env_files:
                    final_files.extend(env_files)

            # 如果选择的模式是ONE，只需要返回一条记录即可；此处做切片取第一条。    
            if select_mode == EnvSelectModeDef.ANY.name:
                final_files = final_files[0:1]

            # 遍历结果，返回调用者。
            for f in final_files:
                logging.info(f"Scan file - ({f})")
                yield f

            # 如果选择的模式是ONE，则已经满足条件，立刻退出；否则需要继续检索所有的满足条件的文件。 
            if final_files and (select_mode == EnvSelectModeDef.ANY.name):
                break