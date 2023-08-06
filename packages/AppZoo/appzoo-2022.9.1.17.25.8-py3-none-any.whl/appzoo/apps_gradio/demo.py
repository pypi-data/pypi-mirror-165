#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AppZoo.
# @File         : demo
# @Time         : 2021/9/6 上午9:51
# @Author       : yuanjie
# @WeChat       : 313303303
# @Software     : PyCharm
# @Description  :
# /Users/yuanjie/Library/Python/3.7/lib/python/site-packages/pip

# <module 'gradio' from '/Users/yuanjie/Library/Python/3.7/lib/python/site-packages/gradio/__init__.py'>


from meutils.pipe import *
import gradio as gr

gr.close_all()


def fn(*args, **kwargs):
    logger.info(args)
    logger.info(kwargs)

    return None


(
    gr.Interface(
        fn=fn,
        inputs=gr.Image(type="file"),
        outputs='text',  # gr.Label(num_top_classes=10),
        interpretation="default",
        title="Demo",
        examples=['2_.png'] * 10,
        # cache_examples=True,
        # live=True,

    )
        .launch(server_name='0.0.0.0', server_port=9955, debug=True, share=True)
)
