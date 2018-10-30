#!/usr/local/miniconda2/bin/python
# _*_ coding:utf-8 _*_
"""
# @Project : docker-dashboard
# @Time    : 2018/10/30 10:46 AM
# @Author  : zhangchengcheng
# @FileName: autoscalingInfo.py
# @Github  : https://github.com/sweetcczhang
"""
from flask import Blueprint, jsonify, request
from kube import scale_client


autoscaling = Blueprint('autoscalingInfo', __name__)


@autoscaling.route('/', methods=['GET', 'POST'])
def get_auto_scale_list():
    return_model = {}
    namespace = request.values.get(key='namespace', default=None)
    try:
        scale_list = scale_client.list_auto_scaling(namespace=namespace)
        if scale_list is not None:
            data = {'length': scale_list[0], 'autoScaleList': scale_list[1]}
            return_model['retCode'] = 200
            return_model['retDesc'] = 'success'
            return_model['data'] = data
        else:
            raise Exception('查询失败')

    except Exception as e:
        print e
        return_model['retCode'] = 500
        return_model['retDesc'] = '查询失败'
    return jsonify(return_model)
