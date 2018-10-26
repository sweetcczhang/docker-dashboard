#!/usr/local/miniconda2/bin/python
# _*_ coding:utf-8 _*_
"""
#
# @Time   : 2018/7/21 15:37
# @Author : 张城城
"""
from flask import Blueprint, jsonify, request

from kube import hostInfo
from kube import pods

hosts = Blueprint('hostInfo', __name__)


@hosts.route('/getHostList')
def get_host_info():
    """
    获取主机列表信息
    :return:
    """

    return_model = {}
    try:
        temp = hostInfo.get_host_info()
        data = {'length': temp[0], 'hosts': temp[1]}
        return_model['retCode'] = 200
        return_model['retDesc'] = 'success'
        return_model['data'] = data

    except Exception as e:
        return_model['retCode'] = 500
        return_model['retDesc'] = '获取消息失败'
        return_model['data'] = None
        print("Exception when calling CoreV1Api->list_node: %s\n" % e)
    return jsonify(return_model)


@hosts.route('/getHostDetail')
def get_host_detail():
    """
    获取主机详细信息
    :return:
    """
    return_model = {}
    host_name = request.args.get(key='hostName', default=None)
    try:
        host_detail = hostInfo.host_detail(host_name=host_name)
        pod_info = pods.get_pod_from_label_or_field(field_selector=host_name)
        if host_detail is not None:
            return_model['retCode'] = 200
            return_model['retDesc'] = 'success'
            data = {'hostInfo': host_detail[1], 'conditions': host_detail[0], 'podNum': pod_info[0],
                    'podsList': pod_info[1]}
            return_model['data'] = data
        else:
            return_model['retCode'] = 500
            return_model['retDesc'] = '主机名错误，或者别的错误，请检查参数'
            return_model['data'] = None
    except Exception as e:
        print e
    return return_model


