from typing import Union
import grpc
import json

from . import ZoneSenderData
from .ObjIo import *

from .Protos import LinParserNode_pb2,LinParserNode_pb2_grpc

class LinParseNodeClient(object) :
    """
    LinParserNode 的客户端
    """
    def __init__(self) -> None:
        self._linDbParserStub = LinParserNode_pb2_grpc.LinParserNodeStub(
            channel=grpc.insecure_channel(
                target='{0}:{1}'
                    .format(
                        ZoneSenderData.LIN_PARSERNODE_NODE_IP, 
                        ZoneSenderData.LIN_PARSERNODE_NODE_PORT),
                options = ZoneSenderData.GRPC_OPTIONS
            )
        )
    
    def setChannelConfig(self,appChannel:int,ldfPath:str,linMode:str,
                            txrecv:int = 0,baudrate:int = 0) -> int:
        ''' 添加一个ldf文件到特定的通道上
        :param appChannel: int vector硬件配置上对应的LIN通道 
        :param ldfPath: str ldf文件的路径
        :param linMode: str 该通道的模式，支持Master,Slave 
        :param txrecv: int 默认全接收，0为全接收，1为接收收到的报文，2为接收发送的报文
        :param baudrate: int 默认19200,波特率
        :return: int\n
            - 0: 成功\n
            - 1: 配置失败\n
            - 1000: error\n
        '''
        try:
            res_ = self._linDbParserStub.SetChannelConfig(
                LinParserNode_pb2.lin_channel_config(
                    ldf_path = ldfPath,
                    lin_mode = linMode,
                    txrecv = txrecv,
                    baudrate = baudrate,
                    lin_channel = appChannel,
                )
            )
            print('setChannelConfig result: {0}, reason: {0}'.format(res_.result, res_.reason))
            return res_.result
        except Exception as e_ :
            print(e_)
            return 1000
    
    def getLdfJson(self) -> Union[dict,int]:
        ''' 获取配置的ldf，并返回解析后的ldf
        :return: dict,int\n
            - dict: 成功\n
            - 1000: error\n
        '''
        try:
            res_ = self._linDbParserStub.GetLdfJsonTree(
                LinParserNode_pb2.Common__pb2.empty()
            )
            print('getLdfJson result: {0}, reason: {0}'.format(res_.result, res_.reason))
            if res_.result == 0 :
                return json.loads(res_.json_data)
            else:
                raise Exception(f'{res_.reason}')
        except Exception as e_ :
            print(e_)
            return 1000

    def clearChannelConfig(self) ->int:
        ''' 清空所有已配置的ldf文件
        :return: int\n
            - 0: 成功\n
            - 1000: error\n
        '''
        try:
            res_ = self._linDbParserStub.ClearDbfile(
                LinParserNode_pb2.Common__pb2.empty()
            )
            return res_.result
        except Exception as e_ :
            print(e_)
            return 1000
    
    def clearSubscribe(self) :
        ''' 清空所有的订阅
        :return: int\n
            - 0: 成功\n
            - 1000: error\n
        '''
        try:
            res_ = self._linDbParserStub.ClearSubscribe(
                LinParserNode_pb2.Common__pb2.empty()
            )
            print('清除所有 LinParser 的订阅 result: {0}, reason: {0}'.format(res_.result, res_.reason))
            return res_.result
        except Exception as e_ :
            print(e_)
            return 1000

    def setFrameSimulation(self,channel:int,frame:Union[int,str],simu:bool) -> int:
        ''' 设置LIN报文仿真
        :param channel: int vector硬件配置上对应的LIN通道
        :param frame: int or str LIN报文的名字或者ID
        :param simu: bool True为仿真，False为关闭仿真
        :return: int\n
            - 0: 成功\n
            - 1: 未找到指定报文
            - 1000: error\n
        '''
        try:
            if isinstance(frame,str) :
                linframe = LinParserNode_pb2.lin_frame_config(
                    frame_name = frame,
                    channel = channel,
                    simu = simu,
                )
            elif isinstance(frame,int) :
                linframe = LinParserNode_pb2.lin_frame_config(
                    frame_id = frame,
                    channel = channel,
                    simu = simu,
                )
            else :
                print(f'frame type unsupport,input type is {type(frame)}')
                return 1000
            res_ = self._linDbParserStub.SetFrameSimulation(linframe)
            print('setFrameSimulation result: {0}, reason: {0}'.format(res_.result, res_.reason))
            return res_.result
        except Exception  as e_ :
            print(e_)
            return 1000

    def setNodeSimulation(self,channel:int,Node:str,simu:bool) -> int:
        ''' 设置LIN节点仿真
        :param channel: int vector硬件配置上对应的LIN通道
        :param Node: str LIN节点的名字
        :param simu: bool True为仿真，False为关闭仿真
        :return: int\n
            - 0: 成功\n
            - 1: 未找到指定的节点
            - 1000: error\n
        '''
        try:
            if isinstance(Node,str) :
                res_ = self._linDbParserStub.SetNodeSimulation(
                    LinParserNode_pb2.lin_node_config(
                        node_name = Node,
                        channel = channel,
                        simu = simu,
                    )
                )
            else :
                print(f'Node type unsupport,input type is {type(Node)}')
                return 1000
            print('setNodeSimulation result: {0}, reason: {0}'.format(res_.result, res_.reason))
            return res_.result
        except Exception  as e_ :
            print(e_)
            return 1000

        

