#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AppZoo.
# @File         : creat_proto
# @Time         : 2022/9/1 下午5:11
# @Author       : yuanjie
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  : 


from meutils.pipe import *

cmd = """
python -m grpc_tools.protoc -I ./ --python_out=./ --grpc_python_out=. base.proto
""".strip()
os.system(cmd)

p = Path('base_pb2_grpc.py')
_ = (
    p.read_text()
        .replace("import base_pb2 as base__pb2", "from appzoo.grpc_app.protos import base_pb2 as base__pb2")
)

p.write_text(_)
