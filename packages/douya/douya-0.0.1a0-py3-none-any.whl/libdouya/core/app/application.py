# -*- coding:utf-8 -*-
#!/usr/bin/env python

import os, sys, logging.config, getopt, time, select, errno, asyncio
from typing import List

from ...definations.cfg import DY_CONFIGURATION_KEY_DEF, EnvDefs, ConfigerDefs
from ...dataclasses.i.rdb import IDatabaseDeclarative
# from ...dataclasses.i.srv import IDyService
from ...dataclasses.c.db.databases import Databases
from ...utilities.tml import TmlUtl
from ...utilities.module import ModuleUtl
from ..srv import ServiceTask
from ..mgr import ConfigurationMgr, NamingMgr, DatacacheMgr


# Windows信号时
# SIGINT      Ctrl+C中断
# SIGILL       非法指令
# SIGFPE      浮点异常
# SIGSEGV   段错误, 非法指针访问
# SIGTERM   kill发出的软件终止
# SIGBREAK Ctrl+Break中断
# SIGABRT   调用abort导致

class DyApplication(object):
    def __init__(self, *import_modules:str):
        self.__import_module_set = set([ m for m in import_modules if m])
        self.__env = None
        self.__env_configurations = []
        self.__configurations = []
        # self.__halt_event = threading.Event()

    def __call__(self):
        self.parse_cmdline()

        self.__import_module_set.update([ m for m in os.environ.get(EnvDefs.APP_MODULE.name, "").split(":") if m ])
        if not self.__import_module_set:
            ModuleUtl.import_module(*list(self.__import_module_set))

        ConfigurationMgr.get_instance().init(self.env, *self.get_env_configurations())
        for c in self.get_configurations():
            ConfigurationMgr.get_instance().merge_configuration(c)

        if log_conf := ConfigurationMgr.get_instance().get_conf(DY_CONFIGURATION_KEY_DEF.LOGGER):
            logging.config.dictConfig(log_conf)
        else:
            logging.basicConfig(format='%(asctime)s - %(pathname)s[line:%(lineno)d] - %(levelname)s: %(message)s', level=logging.INFO)

        logging.debug(str(ConfigurationMgr.get_instance().configuration))

        DatacacheMgr.get_instance().initialize()
        if datacache_configer := ConfigurationMgr.get_instance().try_to_get_configer(ConfigerDefs.DATACACHE.value):
            datacaches = datacache_configer.make_data_caches()
            DatacacheMgr.get_instance().add(*datacaches)

        dbs: Databases = None
        if declaratives := self.get_database_declaratives():
            with ConfigurationMgr.get_instance().get_configer(ConfigerDefs.DB.value) as database_configer:
                dbs = database_configer.initialize_and_get_databases(*declaratives)

        tasks = []
        with ConfigurationMgr.get_instance().get_configer(ConfigerDefs.SRV.value) as service_configer:
            for srv_groups in service_configer.group_services(dbs):
                for srvs in srv_groups:
                    tasks.append(ServiceTask(*srvs))
        if not tasks:
            raise RuntimeError("No service task found")

        logging.info("Startup application")
        # if 'nt' == os.name:
        #     import win32api
        #     win32api.SetConsoleCtrlHandler(self.__quit_win32, 1)
        # else:
        #     import signal
        #     signal.signal(signal.SIGINT, self.__quit_not_win32)
        #     signal.signal(signal.SIGKILL, self.__quit_not_win32)

        # self.__halt_event.clear()
        # for task in tasks:
            # self.__wait_forever()
            # self.__halt_event.wait()

        loop = asyncio.get_event_loop()
        try:
            loop.run_until_complete(asyncio.wait(tasks))
        except (KeyboardInterrupt, ):
            pass
        finally:
            logging.info("Shutdown application")

    # def __wait_forever(self):
    #     # Wait forever
    #     try:
    #         # rfd, wfd = os.pipe()
    #         # os.close(wfd)

    #         while True:
    #             # try:
    #             #     select.select([], [], [])
    #             # except select.error as e:
    #             #     logging.exception("Got some exception")
    #             #     if e.args[0] != errno.EINTR:
    #             #         raise

    #             if os.name == "posix":
    #                 # NOTE(sileht): we cannot use threading.Event().wait(),
    #                 # threading.Thread().join(), or time.sleep() because signals
    #                 # can be missed when received by non-main threads
    #                 # (https://bugs.python.org/issue5315)
    #                 # So we use select.select() alone, we will receive EINTR or
    #                 # will read data from signal_r when signal is emitted and
    #                 # cpython calls PyErr_CheckSignals() to run signals handlers
    #                 # That looks perfect to ensure handlers are run and run in the
    #                 # main thread
    #                 try:
    #                     select.select([self.signal_pipe_r], [], [])
    #                 except select.error as e:
    #                     if e.args[0] != errno.EINTR:
    #                         raise
    #             else:
    #                 # NOTE(sileht): here we do only best effort
    #                 # and wake the loop periodically, set_wakeup_fd
    #                 # doesn't work on non posix platform so
    #                 # 1 seconds have been picked with the advice of a dice.
    #                 time.sleep(1)
    #     except (KeyboardInterrupt, SystemExit):
    #         logging.info('SIGINT or CTRL-C detected. Exiting gracefully')
    #     except:
    #         logging.exception("Got some exception")

    # # def __quit_win32(self, sig):
    # #     logging.info('SIGINT or CTRL-C detected. Exiting gracefully')
    # #     self.__halt_event.set()

    # # def __quit_not_win32(self, signum, frame):
    # #     logging.info('SIGINT or CTRL-C detected. Exiting gracefully')
    # #     self.__waiting_for_stopper_event.set()

    @property
    def exe(self) -> str: return f'{sys.argv[0]}' 

    def get_env(self) -> str: return self.__env
    def set_env(self, env:str): self.__env = env
    env = property(get_env, None, None, "环境")

    def get_usage(self) -> List[str]: return f'{self.exe}'
    # usage = property(get_usage, None, None, "使用说明")

    def get_env_configurations(self) -> List[str]: return self.__env_configurations
    # env_configurations = property(get_env_configurations, None, None, "环境配置")

    def get_configurations(self) -> List[str]: return self.__configurations
    # configurations = property(get_configurations, None, None, "配置")

    def get_database_declaratives(self) -> List[IDatabaseDeclarative]: return None

    def parse_cmdline(self):
        opts, *_ = getopt.getopt(sys.argv[1:], "hc:", ["help", "env=", "configuration-file=", "env-configuration-file="])
        for name, value in opts:
            if name in [ "-h", "--help"]:
                print(self.usage)
                sys.exit(0)
            elif name in [ "--env" ]:
                self.env = value
            elif name in ["-c", "--configuration-file"]:
                self.get_configurations().append(TmlUtl.load(value))
            elif name in ["-c", "--env-configuration-file"]:
                with open(value, 'r', encoding='utf-8') as f:
                    self.get_env_configurations().append(f.read())
