#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AppZoo.
# @File         : test
# @Time         : 2022/3/25 下午4:36
# @Author       : yuanjie
# @WeChat       : 313303303
# @Software     : PyCharm
# @Description  : 


from meutils.pipe import *
from appzoo import App

app = App()
app_ = app.app


# app.add_route('/get', lambda **kwargs: kwargs, method="GET", result_key="GetResult")
# app.add_route('/post', lambda **kwargs: kwargs, method="POST", result_key="PostResult")
#
# app.add_route_plus('/post_test', lambda **kwargs: kwargs, method="POST")
#
# from fastapi import FastAPI, Form, Depends, File, UploadFile, Body, Request, Path
#
# def proxy_app_(kwargs: dict):
#     logger.info(kwargs)
#     print(kwargs)
#     r = requests.request(**kwargs)
#     return r.json()
#l;=]
#
# app.add_route_plus(proxy_app_, methods=["GET", "POST"], data=None)f j a

import time

def f(kwargs):
    return {'a': None, 'b': None, 'c': None, 't': pd.to_datetime('2022-08-03 10:06:45')}

app.add_route_plus(f, methods=["GET", "POST"], data=None)

if __name__ == '__main__':
    app.run(app.app_from(__file__), port=9955, debug=True)


from docarray import Document, DocumentArray

d = Document(uri='https://www.gutenberg.org/files/1342/1342-0.txt').load_uri_to_text()
da = DocumentArray(Document(text=s.strip()) for s in d.text.split('\n') if s.strip())
da.apply(Document.embed_feature_hashing, backend='process')

q = (
    Document(text='she smiled too much')
    .embed_feature_hashing()
    .match(da, metric='jaccard', use_scipy=True)
)

print(q.matches[:5, ('text', 'scores__jaccard__value')])