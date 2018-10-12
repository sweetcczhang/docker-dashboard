#!/usr/local/miniconda2/bin/python
# _*_ coding:utf-8 _*_
"""
# @Project : docker-dashboard
# @Time    : 2018/10/12 上午10:04
# @Author  : zhangchengcheng
# @FileName: basic.py
# @Github  : https://github.com/sweetcczhang
"""
from kube.rest import configKube as conf


class Client(object):

    def __init__(self):
        self.v1_client = conf.get_core_v1_api()
        self.ext_client = conf.get_extensions()

    def v1_client(self):
        return self.v1_client

    def ext_client(self):
        return self.ext_client
