#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AppZoo.
# @File         : service
# @Time         : 2022/8/19 下午5:14
# @Author       : yuanjie
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  : 


import grpc
from appzoo.grpc_app.protos.base_pb2 import Request, Response
from appzoo.grpc_app.protos.base_pb2_grpc import GrpcServiceServicer, GrpcServiceStub, add_GrpcServiceServicer_to_server

from meutils.pipe import *
from pickle import dumps, loads


class Service(GrpcServiceServicer):

    def __init__(self, debug=False):
        self.debug = debug

    def main(self, *args, **kwargs):
        raise NotImplementedError('Method not implemented!')

    @logger.catch()
    def _request(self, request, context):
        input = loads(request.data)
        if self.debug:
            logger.debug(input)

        output = dumps(self.main(input))
        return Response(data=output)

    def run(self, port=8000, max_workers=3):
        options = [
            ('grpc.max_send_message_length', 32 * 1024 * 1024),  # 32 MB
            ('grpc.max_receive_message_length', 32 * 1024 * 1024)
        ]
        server = grpc.server(ThreadPoolExecutor(max_workers), options=options)  # compression = None
        add_GrpcServiceServicer_to_server(self, server)

        server.add_insecure_port(f'[::]:{port}')
        server.start()
        logger.info("GrpcService Running ...")
        server.wait_for_termination()

        # try:
        #     while 1:
        #         time.sleep(60 * 60 * 24)
        # except KeyboardInterrupt:
        #     server.stop(0)


if __name__ == '__main__':
    class MyService(Service):

        def main(self, data):
            return data


    MyService(debug=False).run()
