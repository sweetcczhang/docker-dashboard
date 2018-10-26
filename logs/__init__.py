#!/usr/local/miniconda2/bin/python
# _*_ coding:utf-8 _*_
"""
# @Project : docker-dashboard
# @Time    : 2018/10/17 下午8:56
# @Author  : zhangchengcheng
# @FileName: __init__.py.py
# @Github  : https://github.com/sweetcczhang
"""

from logs.node_logs import NodeLogs

from logs.pod_logs import PodLogs

nodeLogs = NodeLogs()

podLogs = PodLogs()
