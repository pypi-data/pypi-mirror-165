# -*- coding:utf-8 -*-
#!/usr/bin/env python

from ....definations.cfg import DY_CONFIGURATION_KEY_DEF, EnvDefs

ENVIRONMENT_MAPPING_CONFIGURATION_DFLT_DEF = f"""
[[envs]]
name = "{EnvDefs.APP_WORK_DIR.name}"
type = "string"

[[envs]]
name = "{EnvDefs.APP_ENV.name}"
type = "string"

[[envs]]
name = "{EnvDefs.APP_CFG_DIR.name}"
type = "string"

[[envs]]
name = "{EnvDefs.APP_CFG_NAME.name}"
type = "string"

[[envs]]
name = "{EnvDefs.APP_LOOKUP_DIR.name}"
type = "string"

[[envs]]
name = "{EnvDefs.APP_HOST.name}"
type = "string"
paths = ["{DY_CONFIGURATION_KEY_DEF.HTTP_SERVICE_HOST}"]

[[envs]]
name = "{EnvDefs.APP_PORT.name}"
type = "integer"
paths = ["{DY_CONFIGURATION_KEY_DEF.HTTP_SERVICE_PORT}"]

[[envs]]
name = "{EnvDefs.APP_DB_URL.name}"
type = "string"
paths = ["{DY_CONFIGURATION_KEY_DEF.PRIMARY_DATABASE_URL}"]

[[envs]]
name = "{EnvDefs.APP_CATALOG_DATA_DIR.name}"
type = "string"
paths = ["{DY_CONFIGURATION_KEY_DEF.DATA_CATALOG_DIR}"]
"""

CONFIGURATION_DFLT_DEF = f'''
[{DY_CONFIGURATION_KEY_DEF.HTTP_SERVICE}]
{DY_CONFIGURATION_KEY_DEF.HTTP_SERVICE_HOST[len(DY_CONFIGURATION_KEY_DEF.HTTP_SERVICE)+1:]} = "127.0.0.1"
{DY_CONFIGURATION_KEY_DEF.HTTP_SERVICE_PORT[len(DY_CONFIGURATION_KEY_DEF.HTTP_SERVICE)+1:]} = 8000
debug = false

[{DY_CONFIGURATION_KEY_DEF.PRIMARY_DATABASE}]
url = "sqlite://"
is_debugging = false
options = [ "creating_tables" ]
db_dir = ""

[{DY_CONFIGURATION_KEY_DEF.CATALOG}]
{DY_CONFIGURATION_KEY_DEF.BINARY_CATALOG_DIR[len(DY_CONFIGURATION_KEY_DEF.CATALOG)+1:]} = "bin"
{DY_CONFIGURATION_KEY_DEF.TEMPORARY_CATALOG_DIR[len(DY_CONFIGURATION_KEY_DEF.CATALOG)+1:]} = "tmp"
{DY_CONFIGURATION_KEY_DEF.BACKUP_CATALOG_DIR[len(DY_CONFIGURATION_KEY_DEF.CATALOG)+1:]} = "bak"
{DY_CONFIGURATION_KEY_DEF.DATA_CATALOG_DIR[len(DY_CONFIGURATION_KEY_DEF.CATALOG)+1:]} = "var"
{DY_CONFIGURATION_KEY_DEF.RUN_CATALOG_DIR[len(DY_CONFIGURATION_KEY_DEF.CATALOG)+1:]} = "run"

[{DY_CONFIGURATION_KEY_DEF.LOGGER}]
version = 1
disable_existing_loggers = false

[{DY_CONFIGURATION_KEY_DEF.LOGGER}.formatters.startdard_fmt]
format = "%(asctime)s | %(process)d:%(thread)d | %(levelname)s | (%(name)s)[%(filename)s:%(lineno)d] | %(message)s"
datefmt = "%Y-%m-%d %H:%M:%S"
[{DY_CONFIGURATION_KEY_DEF.LOGGER}.formatters.http_access_fmt]
format = "%(asctime)s | %(process)d:%(thread)d | %(levelname)s | (%(name)s)[%(filename)s:%(lineno)d] | [%(host)s]: %(request)s %(message)s %(status)d %(byte)d"
datefmt = "%Y-%m-%d %H:%M:%S"

[{DY_CONFIGURATION_KEY_DEF.LOGGER}.handlers.debug_console_handler]
class = "logging.StreamHandler"
level = "DEBUG"
formatter = "startdard_fmt"
stream = "ext://sys.stdout"

[{DY_CONFIGURATION_KEY_DEF.LOGGER}.handlers.generic_handler]
class = "concurrent_log_handler.ConcurrentRotatingFileHandler"
level = "INFO"
formatter = "startdard_fmt"
filename = "app.log"
mode = "a"
encoding = "utf-8"
maxBytes = {10 * 1024 * 1024}
backupCount = 10

[{DY_CONFIGURATION_KEY_DEF.LOGGER}.handlers.fault_handler]
class = "concurrent_log_handler.ConcurrentRotatingFileHandler"
level = "ERROR"
formatter = "startdard_fmt"
filename = "error.log"
mode = "a"
encoding = "utf-8"
maxBytes = {10 * 1024 * 1024}
backupCount = 10

[{DY_CONFIGURATION_KEY_DEF.LOGGER}.handlers.http_access_handler]
class = "concurrent_log_handler.ConcurrentRotatingFileHandler"
level = "NOTSET"
formatter = "http_access_fmt"
filename = "http.log"
mode = "a"
encoding = "utf-8"
maxBytes = {10 * 1024 * 1024}
backupCount = 10

[{DY_CONFIGURATION_KEY_DEF.LOGGER}.root]
level = "NOTSET"
handlers = [ "debug_console_handler", "generic_handler", "fault_handler" ]

[{DY_CONFIGURATION_KEY_DEF.LOGGER}.loggers."sanic.access"]
qualname = "sanic.access"
level = "NOTSET"
propagate = false
handlers = [ "debug_console_handler", "http_access_handler"]
'''