import typing
from pathlib import Path

import grpc

from . import ZoneSenderData
from .ObjIo import *
from .Protos import LogReplayNode_pb2, LogReplayNode_pb2_grpc
from .BlfIo import BlfIoObjs


class LogReplayNodeClient(object):
    def __init__(self) -> None:
        '''
        ZoneSender 用于记录和回放的客户端
        '''
        self._logReplayStub = LogReplayNode_pb2_grpc.LogReplayNodeStub(
            channel=grpc.insecure_channel(
                target='{0}:{1}'.format(ZoneSenderData.LOG_REPLAY_NODE_IP, ZoneSenderData.LOG_REPLAY_NODE_PORT),
                options=ZoneSenderData.GRPC_OPTIONS
            )
        )

    def AddLinDecodeRole(
        self, 
        channels: typing.List[int],
        ldfs: typing.List[str],
        **kwargs) -> int:
        '''
        添加一个 LIN 数据的解析规则
        可以重复添加
        :param channels:list[int] LIN 通道列表
        :param ldfs:list[int] ldf 文件列表
        :return:int
            - 0: 添加成功
            - 1000: raise
        '''
        try:
            ldfs = [str(Path(x_).absolute()) for x_ in ldfs]
            res_ = self._logReplayStub.AddLinDecodeRole(LogReplayNode_pb2.lin_decode_role(
                channels = channels,
                ldfs = ldfs,
            ))
            print(res_.reason)
            return res_
        except Exception as e_:
            print('LogReplayNodeClient.AddLinDecodeRole Exception reason {0}'.format(e_))
            return 1000

    def AddCanDecodeRole(
        self,
        can_db_file_path:str,
        channels:typing.List[int],
        cluster_names:typing.List[str],
        **kwargs
        ) -> int:
        '''
        添加一个 CAN 数据的解析规则
        可以重复添加
        :param can_db_file_path:str CAN DB 文件的路径
        :param channels:list[int] LIN 通道列表
        :param ldfs:list[int] ldf 文件列表
        :return:int
            - 0: 添加成功
            - 1000: raise
        '''
        try:
            res_ = self._logReplayStub.AddCanDecodeRole(LogReplayNode_pb2.can_decode_role(
                can_db_file_path = str(Path(can_db_file_path).absolute()),
                channels = channels,
                cluster_names = cluster_names,
            ))
            print(res_.reason)
            return res_
        except Exception as e_:
            print('LogReplayNodeClient.AddCanDecodeRole Exception reason {0}'.format(e_))
            return 1000

    def Reset(self) -> int:
        '''
        复位
            - 清空解析配置文件
            - 关闭所有正在解析的文件
        :return:int
            - 0: 复位成功
            - 1000: raise
        '''
        try:
            res_ = self._logReplayStub.Reset(LogReplayNode_pb2.Common__pb2.empty())
            print(res_.reason)
            return res_.result
        except Exception as e_:
            print('LogReplayNodeClient.Reset Exception reason {0}'.format(e_))
            return 1000

    def DecodeAny(
        self,
        obj: BlfIoObjs.BlfIoStruct, 
        d_return:dict) -> int:
        '''
        根据设定的规则解包任何 BlfObj
        :param obj:BlfIoObjs.BlfIoStruct 要解包的 blf_obj
        :param d_return:dict 如果解包成功，就返回解包后的结果
        :return:int
            - 0: 解包成功
            - 1000: raise
        '''
        try:
            assert (isinstance(
                obj, 
                (BlfIoObjs.LinMessagePy, 
                BlfIoObjs.CanMessagePy, 
                BlfIoObjs.CanFdMessage64Py, 
                BlfIoObjs.CanFdMessagePy))), 'LogReplayNodeClient.DecodeAny.obj 的类型不受支持'
            return 0
        except Exception as e_:
            print('LogReplayNodeClient.DecodeAny Exception reason {0}'.format(e_))
            return 1000

