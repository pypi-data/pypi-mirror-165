#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AppZoo.
# @File         : demo
# @Time         : 2022/5/30 下午3:19
# @Author       : yuanjie
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  : 


from meutils.pipe import *
from appzoo import App
from meutils.str_utils import json_loads

app = App()
app_ = app.app


@lru_cache()
def post_func(kwargs: str):
    logger.info(kwargs)
    return json_loads(kwargs)


@lru_cache()
def post_func2(kwargs: tuple):  # 这个更快
    logger.info(kwargs)
    return dict(kwargs)


app.add_route_plus(post_func, methods='GET')
app.add_route_plus(post_func2, methods='GET')

if __name__ == '__main__':
    app.run(app.app_from(__file__), port=9955, debug=True)
