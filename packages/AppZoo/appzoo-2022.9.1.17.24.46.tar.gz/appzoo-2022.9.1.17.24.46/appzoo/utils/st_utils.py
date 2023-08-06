#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AppZoo.
# @File         : st_utils
# @Time         : 2021/10/12 下午8:44
# @Author       : yuanjie
# @WeChat       : 313303303
# @Software     : PyCharm
# @Description  : 

import streamlit as st
from streamlit.components.v1 import html, iframe
from meutils.pipe import *


def st_file_uploader(label='上传文件', func=lambda f: f.read()):
    """
        st.dataframe(st_file_uploader(func=pd.read_csv))

    :param label:
    :param func: pd.read_csv(uploaded_file)
    :return:
    """
    uploaded_file = st.file_uploader(label)  # uploaded_file.name

    if uploaded_file and func is not None:  # io.BufferedReader
        return func(uploaded_file)  # bytes_data



# st.sidebar._iframe('http://yuanjie-mac.local:8050/')
# iframe('http://yuanjie-mac.local:8050/', 1024, 1024, 1)
