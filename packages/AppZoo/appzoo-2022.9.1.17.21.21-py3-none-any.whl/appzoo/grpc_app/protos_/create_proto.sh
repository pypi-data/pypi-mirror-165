#!/usr/bin/env bash
# @Project      : AppZoo
# @Time         : 2022/8/19 下午4:31
# @Author       : yuanjie
# @Email        : 313303303@qq.com
# @Software     : PyCharm
# @Description  : ${DESCRIPTION}

python -m grpc_tools.protoc -I ./ --python_out=./ --grpc_python_out=. base.proto