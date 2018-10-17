#!/usr/local/miniconda2/bin/python
# _*_ coding:utf-8 _*_
"""
# @Project : docker-dashboard
# @Time    : 2018/10/15 上午11:36
# @Author  : zhangchengcheng
# @FileName: kube_replicas_set.py
# @Github  : https://github.com/sweetcczhang
"""
from kube import basic
from kubernetes.client.rest import ApiException
from kubernetes import client
import os


class ReplicasSet(basic.Client):
    lists = []