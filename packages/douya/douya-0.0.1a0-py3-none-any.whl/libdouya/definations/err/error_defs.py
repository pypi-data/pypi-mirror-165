# -*- coding:utf-8 -*-
#!/usr/bin/env python

"""
    error_defs.py - 错误码相关的枚举
"""

import typing
from enum import Enum,unique

@unique
class ErrorDefs(Enum):
    SUCCESS = 0 # 失败
    FAILED = 1 # 失败
    BUSY = 2 # 服务繁忙
    TIMEOUT = 3 # 业务超时
    UNKNOWN_ERROR = 4 # 未知错误
    UNDEFINED_ERROR = 5 # 未定义错误
    ILLEGAL_ARGUMENT = 6 # 非法的参数
    NOT_IMPLEMENTED = 7 # 业务未实现
    UNSUPPORTED = 8 # 不支持该业务
    BUSINESS_FAILURE = 9 # 业务失败
    WAIT_DATA_TIMEOUT = 10 # 等待数据超时
    NO_AUTHORIZED = 64 # 未授权
    AUTHORIZE_FAILED = 65 # 鉴权失败
    AUTHORIZE_TIMEOUT = 66 # 鉴权超时
    FORBIDDEN = 67 # 禁止
    NO_USER = 128 # 用户不存在
    USER_UNLOGIN = 129 # 用户未登录
    USER_EXCEPTION = 130 # 用户异常
    USER_SESSION_TIMEOUT = 131 # 用户会话超时
    USER_SESSION_NOT_MATCHED = 132 # 会话不是用户的
    USER_SESSION_NOT_EXIST = 133 # 用户会话不存在
    USER_GET_FUNCTIONAL_PERMISSIONS_FAILED = 134 # 获取功能权限失败
    USER_DENY_TO_VISIT_FUNCTIONS = 135 # 用户禁止使用功能
    USER_GET_MENUS_PERMISSIONS_FAILED = 136 # 获取菜单权限失败
    USER_DENY_TO_VISIT_MENUS = 137 # 用户禁止访问菜单
    USER_GET_RESOURCES_PERMISSIONS_FAILED = 138 # 获取资源权限失败
    USER_DENY_TO_VISIT_RESOURCES = 139 # 用户禁止访问资源
    CONFIG_FAILED = 192 # 配置
    WRITE_CONFIGURE_FILE_FAILED = 193 # 写配置文件失败
    READ_CONFIGURE_FILE_FAILED = 194 # 读配置文件失败
    ILLEGAL_CONFIGURE_FILE_FAILED = 195 # 配置文件格式不合法
    CONFIGURE_FILE_NOT_EXIST = 196 # 配置文件不存在
    PARSE_CONFIGURATION_FAILED = 197 # 解析配置信息失败
    INVALID_CONFIGURATION = 198 # 无效的配置信息失败
    UNKNOWN_CONFIGURATION_FORMAT = 199 # 未知的配置格式
    UNSUPPORTED_CONFIGURATION_FORMAT = 200 # 不支持的配置格式
    GET_DEFAULT_CONFIG_FAILED = 201 # 获取默认配置失败
    SAVE_CONFIG_FAILED = 202 # 保存配置失败
    UPDATE_CONFIG_FAILED = 203 # 更新配置失败
    DELETE_CONFIG_FAILED = 204 # 删除配置失败
    QUERY_CONFIG_FAILED = 205 # 获取配置失败
    RESTORE_CONFIG_FAILED = 206 # 还原配置失败
    CLEAR_CONFIGS_FAILED = 207 # 清除配置失败
    OPERATING_RESOURCES_FAILED = 256 # 资源操作失败
    OPERATING_OBJECTS_FAILED = 257 # 对象操作失败
    AWAITING_RESOURCES_TIMEOUT = 258 # 等待资源超时
    AWAITING_OBJECTS_TIMEOUT = 259 # 等待对象超时
    QUERYING_RESOURCES_FAILED = 260 # 资源查询失败
    QUERYING_OBJECTS_FAILED = 261 # 对象查询失败
    QUERYING_ALL_RESOURCES_FAILED = 262 # 资源全部查询失败
    QUERYING_ALL_OBJECTS_FAILED = 263 # 对象全部查询失败
    QUERYING_RESOURCES_BY_PAGING_FAILED = 264 # 资源分页查询失败 
    QUERYING_OBJECTS_BY_PAGING_FAILED = 265 # 对象分页查询失败 
    QUERYING_RESOURCES_BY_CONDITION_FAILED = 266 # 资源条件查询失败
    QUERYING_OBJECTS_BY_CONDITION_FAILED = 267 # 对象条件查询失败
    RESOURCES_BUSY = 268 # 资源正忙
    OBJECTS_BUSY = 269 # 对象正忙
    RESOUCES_NOT_EXISTS = 270 # 资源不存在
    OBJECTS_NOT_EXISTS = 271 # 对象不存在
    RESOUCES_HAS_ALREADY_EXISTED = 272 # 资源已经存在
    OBJECTS_HAS_ALREADY_EXISTED = 273 # 对象已经存在
    LABEL_QUERY_FAILED = 274 # 标签检索失败
    APP_QUERY_FAILED = 275 # 应用检索失败
    SERVER_QUERY_FAILED = 276 # 服务器检索失败
    SERVICE_QUERY_FAILED = 277 # 服务检索失败
    COMPONENT_QUERY_FAILED = 278 # 组件检索失败
    STORAGE_SERVICE_QUERY_FAILED = 279 # 存储服务检索失败
    STORAGE_POLL_QUERY_FAILED = 280 # 存储池检索失败
    USER_QUERY_FAILED = 281 # 用户检索失败
    ROLE_QUERY_FAILED = 282 # 角色检索失败
    ORIGINATION_QUERY_FAILED = 283 # 组织检索失败
    SUPERIOR_ORG_QUERY_FAILED = 284 # 上级组织检索失败 
    CAMERA_QUERY_FAILED = 285 # 监控点检索失败
    CROSS_QUERY_FAILED = 286 # 卡口检索失败
    LANE_QUERY_FAILED = 287 # 车道检索失败 
    SCREEN_QUERY_FAILED = 288 # 诱导屏检索失败
    ARG_VALIDATION_FAILED = 320 # 参数校验失败
    INVALID_ARG_FORMAT = 321 # 参数格式不合法
    ARGS_LIMIT_CHARS_FORMAT = 322 # 参数字符格式限制
    ARGS_CONTAINS_ILLEGAL_CHARS = 323 # 参数包含不合法字符
    ARGS_CANNOT_EMPTY = 324 # 参数不能为空
    ARGS_MUSTBE_EMPTY = 325 # 参数必须为空
    ARGS_CANNOT_NULL = 326 # 参数不能为null
    ARGS_MUSTBE_NULL = 327 # 参数必须为null
    ARGS_NOT_EXISTS = 328 # 参数不存在
    ARGS_HAS_ALREADY_EXISTED = 329 # 参数已经存在
    ARGS_TOO_LONG = 330 # 参数过长
    ARGS_TOO_SHORT = 331 # 参数过短
    ARGS_LENGHT_OUT_OF_RANGE = 332 # 参数长度在一定范围
    ARGS_OUT_OF_RANGE = 333 # 超过数值指定范围
    ARGS_VALUE_ISNOT_EXPECTED = 334 # 参数非期望的值
    ARGS_VALUE_GE = 335 # 参数取值大于等于固定值
    ARGS_VALUE_G = 336 # 参数取值大于固定值
    ARGS_VALUE_LE = 337 # 参数取值小于等于固定值
    ARGS_VALUE_L = 338 # 参数取值小于固定值
    ARGS_VALUE_E = 339 # 参数取值必需等于固定值
    ARGS_VALUE_NE = 340 # 参数取值不等于固定值
    ARGS_VALUE_GE_LE = 341 # 参数取值在左右闭区间
    ARGS_VALUE_G_L = 342 # 参数取值在左右开区间
    ARGS_VALUE_G_LE = 343 # 参数取值在左开右闭区间
    ARGS_VALUE_GE_L = 344 # 参数取值在左闭右开区间
    ARGS_MUSTBE_EXIST = 345 # 参数必需存在
    ARGS_MUSTBE_EXIST_AND_LENGHT_RANGE = 346 # 参数必需且长度在一定范围
    ARGS_MUSTBE_EXIST_AND_VALUE_RANGE = 347 # 参数必需且取值在一定范围
    ARGS_MUSTBE_EXIST_AND_VALUE_GE = 348 # 参数必需且取值大于等于固定值
    ARGS_MUSTBE_EXIST_AND_VALUE_G = 349 # 参数必需且取值大于固定值
    ARGS_MUSTBE_EXIST_AND_VALUE_LE = 350 # 参数必需且取值小于等于固定值
    ARGS_MUSTBE_EXIST_AND_VALUE_L = 351 # 参数必需且取值小于固定值
    ARGS_MUSTBE_EXIST_AND_VALUE_E = 352 # 参数必需且取值必需等于固定值
    ARGS_MUSTBE_EXIST_AND_VALUE_NE = 353 # 参数必需且取值不等于固定值
    ARGS_MUSTBE_EXIST_AND_VALUE_GE_LE = 354 # 参数必需且取值在左右闭区间
    ARGS_MUSTBE_EXIST_AND_VALUE_G_L = 355 # 参数必需且取值在左右开区间
    ARGS_MUSTBE_EXIST_AND_VALUE_G_LE = 356 # 参数必需且取值在左开右闭区间
    ARGS_MUSTBE_EXIST_AND_VALUE_GE_L = 357 # 参数必需且取值在左闭右开区间
    DB_OPERATE_FAILED = 384 # 数据库操作失败
    CONN_DB_FAILED = 385 # 连接数据库失败
    GET_DB_CONNECTOR_FAILED = 386 # 获取数据库连接句柄失败
    BEYOND_DB_MAX_SESSIONS = 387 # 超过最大会话数
    MQ_OPERATE_FAILED = 448 # 消息队列操作失败 
    PUSH_TO_QUEUE_FAILED = 449 # 推送消息到消息队列失败
    POLL_FROM_QUEUE_FAILED = 450 # 从消息队列获取消息失败
    SUBSCRIBE_QUEUE_FAILED = 451 # 推送消息到消息队列失败
    DICTIONARY_QUERY_FAILED = 512 # 字典检索失败
    DICTIONARY_GROUP_QUERY_FAILED = 513 # 字典检索失败 
    DATA_EXPORT_FAILED = 576 # 数据导出失败 
    NO_DATA_CAN_BE_EXPORTED = 577 # 没有数据可以导出
    ALL_DATA_EXPORTED_FAILED = 578 # 所有数据导出失败
    NO_PERMIT_EXPORT_DATA = 579 # 没有权限导出数据
    NO_PERMIT_EXPORT_ALL_DATA = 580 # 没有权限导出所有数据
    DATA_LOAD_FAILED = 581 # 数据导入失败 
    NO_DATA_CAN_BE_LOADED = 582 # 没有数据可以导入
    ALL_DATA_LOADED_FAILED = 583 # 所有数据导入失败
    NO_PERMIT_LOAD_DATA = 584 # 没有权限导入数据
    NO_PERMIT_LOAD_ALL_DATA = 585 # 没有权限导入所有数据
    IO_EXCEPTION = 640 # IO异常
    INVALID_IO_HANDLE = 641 # 无效的IO句柄
    OBTAIN_FILE_FAILED = 642 # 获取文件失败
    OBTAIN_FILE_STATUS_FAILED = 643 # 获取文件状态失败
    NO_FILE_FOUND = 644 #找不到文件
    OPEN_FILE_FAILED = 645 # 打开文件失败
    CLOSE_FILE_FAILED = 646 # 关闭文件失败
    DELETE_FILE_FAILED = 647 # 删除文件失败
    NETWORK_EXCEPTION = 704 # 网络异常
    REQUEST_TIMEOUT_EXCEPTION = 705 # 请求超时
    CONNECTION_EXCEPTION = 706 # 设备或服务器连接异常
    DONWLOAD_FILE_FAILED = 707 # 下载文件失败
    UPLOAD_FILE_FAILED = 708 # 上传文件失败
    MESSAGE_QUEUE_OPERATE_FAILED = 709 # 消息队列操作失败
    EXTENSION_ERROR = 65535 # 扩展错误信息

    def __repr__(self):
        return "0x%x" % (self.value)

    def __str__(self):
        return self.name