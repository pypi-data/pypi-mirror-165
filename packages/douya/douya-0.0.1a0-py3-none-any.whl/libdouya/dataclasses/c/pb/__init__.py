# # -*- coding:utf-8 -*-
# #!/usr/bin/env python

# from abc import ABCMeta, abstractmethod
# from liberror.errorcode import Errorcode
# from liberror.svc.any import ErrorcodeE
# from google.protobuf.any_pb2 import Any 
# from libhpp.api.pb.eo.c.pub_pb2 import Rp,Rq,Metadata,Statusdata

# class RqApi(metaclass = ABCMeta):
#     def __init__(self): pass

#     @staticmethod
#     def metadata(rq):
#         return rq.metadata

#     @staticmethod
#     def data(rq, clzz):
#         o = clzz()
#         rq.data.Unpack(o)
#         return o

#     @staticmethod
#     def xdata(rq, *clzzs):
#         # online = WeChatOnlineNoticeMessage_pb2.WeChatOnlineNoticeMessage()
#         # tmessage.Content.Unpack(online)
#         for clzz in clzzs:
#             if rq.data.Is(clzz.DESCRIPTOR):
#                 o = clzz()
#                 rq.data.Unpack(o)
#                 return o
#         else:
#             raise ErrorcodeE.FAILED.ec().exception().append('Failed to parse message')

#     @staticmethod
#     def by_http(http_rq):
#         rp = Rp()
#         rp.version = http_rq.version
#         if http_rq.metadata:
#             rp.metadata = Metadata()
#         return rp

#     @staticmethod
#     def request(data, metadata = None):
#         rq = Rq()
#         rq.version = 'v1'
#         if isinstance(metadata, Metadata):
#             rq.metadata = metadata
#         rq.data.Pack(data)
#         return rq

# class RpApi(metaclass = ABCMeta):
#     def __init__(self): pass

#     @staticmethod
#     def successful(rp):
#         if not rp.statusdata:
#             return False
#         if not rp.statusdata.code.startswith('0x') or not self.statusdata.code.startswith('0X'):
#             return False

#         try:
#             return int(rp.statusdata.code[2:], 16) == ErrorcodeE.SUCCESS.value
#         except:
#             return False

#     @staticmethod
#     def success(*datas):
#         ec = ErrorcodeE.SUCCESS.ec()
#         return RpApi.fail(ec, *datas)

#     @staticmethod
#     def fail(ec: Errorcode,  *datas):
#         rp = Rp()
#         rp.version = "v1"
#         rp.statusdata.code = '0x%x' %(ec.id)
#         rp.statusdata.message = str(ec)
#         rp.statusdata.label = ''
#         rp.statusdata.prompt = ec.prompt if ec.prompt else ''
#         for d in datas:
#             o = Any()
#             o.Pack(d)
#             rp.datas.append(o)
#         return rp

#     @staticmethod
#     def metadata(rp):
#         return rp.metadata

#     @staticmethod
#     def datas(rp, clzz):
#         succeeding_datas, failing_datas = [], []
#         for data in rp.datas:
#             if data.Is(clzz.DESCRIPTOR):
#                 o = clzz()
#                 data.Unpack(o)
#                 succeeding_datas.append(o)
#             else:
#                 failing_datas.append(data)
#         return succeeding_datas,failing_datas

#     @staticmethod
#     def xdatas(rp, *clzzs):
#         # online = WeChatOnlineNoticeMessage_pb2.WeChatOnlineNoticeMessage()
#         # tmessage.Content.Unpack(online)
#         succeeding_datas, failing_datas = [], []
#         for data in rp.datas:
#             for clzz in clzzs:
#                 if data.Is(clzz.DESCRIPTOR):
#                     o = clzz()
#                     data.Unpack(o)
#                     succeeding_datas.append(o)
#             else:
#                 failing_datas.append(data)
#         return succeeding_datas,failing_datas