#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AppZoo.
# @File         : client
# @Time         : 2022/8/19 下午5:15
# @Author       : yuanjie
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  : 


import grpc
from appzoo.grpc_app.protos.base_pb2 import Request, Response
from appzoo.grpc_app.protos.base_pb2_grpc import GrpcServiceServicer, GrpcServiceStub, add_GrpcServiceServicer_to_server

from pickle import dumps, loads


class Client(object):

    def __init__(self, ip='0.0.0.0', port=8000):
        options = [
            ('grpc.max_send_message_length', 32 * 1024 * 1024),  # 32 MB
            ('grpc.max_receive_message_length', 32 * 1024 * 1024)
        ]
        self.conn = grpc.insecure_channel(f"{ip}:{port}", options=options)
        self._client = GrpcServiceStub(channel=self.conn)

    def request(self, data):
        input = dumps(data)
        request = Request(data=input)
        response = self._client._request(request)
        output = loads(response.data)

        return output


if __name__ == '__main__':
    client = Client()

    import sys
    i = ['1, 2, 3, 4', 'as']*10000
    print(sys.getsizeof(dumps(i)) / 1024 ** 2)
    _ = client.request(i)
    # print(_)
