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
import json
import os

autoscaling = Blueprint('autoscalingInfo', __name__)


@autoscaling.route('/getAutoScaleList', methods=['GET', 'POST'])
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


@autoscaling.route('/createAutoScale', methods=['GET', 'POST'])
def create_auto_scale():
    return_model = {}
    try:
        namespace = request.values.get(key='namespaces', default='default')
        name = request.values.get(key='name')
        labels = request.values.get(key='labels')
        deploy_name = request.values.get(key='deployName')
        min_replicas = int(request.values.get(key='minReplicas', default=1))
        max_replicas = int(request.values.get(key='maxReplicas', default=10))
        metrics = request.values.get(key='metric')

        result = scale_client.create_auto_scale(namespace=namespace, name=name, labels=labels, deploy_name=deploy_name,
                                                min_replicas=min_replicas, max_replicas=max_replicas, metrics=metrics)
        if result is not None:
            return_model['retCode'] = 200
            return_model['retDesc'] = 'success'
        else:
            raise Exception('创建自动伸缩器失败')

    except Exception as e:
        print e
        return_model['retCode'] = 500
        return_model['retDesc'] = '创建自动伸缩器失败'
    return jsonify(return_model)


@autoscaling.route('/labelAutoScale', methods=['GET', 'POST'])
def label_auto_scale():
    return_model = {}
    name = request.values.get(key='name')
    namespace = request.values.get(key='namespace', default='default')
    labels = request.values.get(key='labels')
    labels = labels.encode('utf-8')
    labels = json.loads(labels)
    label = []
    for l in labels:
        temp = l['key'] + '=' + l['value']
        label.append(temp)
    result = ''
    try:
        for la in label:
            commands = 'kubectl label hpa ' + name + ' -n ' + namespace + la
            output = os.popen(commands)
            result = request + output.read()
        return_model['retCode'] = 200
        return_model['retDesc'] = 'success'
        return_model['data'] = result
    except Exception as e:
        print e
        return_model['retCode'] = 500
        return_model['retDesc'] = 'hpa打标签失败'

    return jsonify(return_model)
