#!/usr/local/miniconda2/bin/python
# _*_ coding:utf-8 _*_
"""
# @Project : docker-dashboard
# @Time    : 2018/10/25 下午10:38
# @Author  : zhangchengcheng
# @FileName: logs_info.py
# @Github  : https://github.com/sweetcczhang
"""
from flask import Blueprint, jsonify, request
from logs import nodeLogs, podLogs
logs = Blueprint('logs_info', __name__)


@logs.route("/getNodeLogs")
def get_node_logs():
    return_model = {}
    host_ip = request.values.get(key='hostIp', default=None)
    data = nodeLogs.node_data(ip=host_ip)
    return_model['retCode'] = 200
    return_model['retDesc'] = 'success'
    return_model['data'] = data

    return jsonify(return_model)


@logs.route("/getPodLogs")
def get_pod_logs():
    return_model = {}
    namespace = request.args.get(key='namespace', default='default')
    name = request.args.get(key='podName', default=None)
    if name is None:
        return_model['retCode'] = 500
        return_model['retDesc'] = '参数错误，pod名称不能为空'
    else:
        data = podLogs.pod_data(namespace=namespace, pod_name=name)
        return_model['retCode'] = 200
        return_model['retDesc'] = 'success'
        return_model['data'] = data
    return jsonify(return_model)
