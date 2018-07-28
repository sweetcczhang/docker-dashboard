#!/usr/local/miniconda2/bin/python
# _*_ coding:utf-8 _*_
"""
# @Time   : 2018/7/11 23:49
# @Author : 张城城
"""
from flask import Blueprint, jsonify, request, Response
from kubernetes import client, config
from kubernetes.client.rest import ApiException
from pprint import pprint
import json
pods = Blueprint('kube', __name__)


def config1():
    config.load_kube_config(config_file='/root/zcc/hello/config')
    v1 = client.CoreV1Api()
    return v1


@pods.route('/listPods')
def get_all_pods():
    return_model = {}
    v1 = config1()
    print ("Listing pods with their ips:")
    try:
        ret = v1.list_pod_for_all_namespaces()
        list1 = []
        pprint(ret)
        for i in ret.items:
            print("%s\t%s\t%s\t%s" % (i.metadata.name, i.metadata.namespace, i.status.host_ip, i.status.pod_ip))
            temp = {'name': i.metadata.name, 'namespace': i.metadata.namespace, 'host_ip': i.status.host_ip,
                    'startTime': i.status.start_time, 'image': i.spec.containers[0].image, 'status': i.status.phase}
            list1.append(temp)

        return_model['data'] = list1
        return_model['retCode'] = 200
        return_model['retDesc'] = 'success'
        return jsonify(return_model)
    except ApiException as e:
        print("Exception when calling CoreV1Api->list_pod_for_all_namespaces: %s\n" % e)


@pods.route('/getPodLog')
def get_namespaced_pod_log():
    '''
    获取pod的输出日志
    :return:
    '''
    return_model = {}
    v1 = config1()
    name = request.args.get('name')
    tail_lines = request.args.get('tail_lines', 100)
    namespace = request.args.get('namespace', default='default')
    print ("Listing pods with their ips:")
    try:
        resouce = v1.read_namespaced_pod_log(name=name, namespace=namespace, tail_lines=tail_lines)
        pprint(resouce)
        return_model['retCode'] = 200
        return_model['retDesc'] = 'success'
        return_model['data'] = resouce

    except ApiException as e:
        return_model['retCode'] = 500
        return_model['retDesc'] = 'Exception when calling CoreV1Api->list_pod_for_all_namespaces'
        return_model['data'] = ''
        print("Exception when calling CoreV1Api->list_pod_for_all_namespaces: %s\n" % e)

    return jsonify(return_model)


@pods.route('/status')
def get_namespace_pod_status():

    v1 = config1()
    try:
        status = v1.read_namespaced_pod_status(name='nodedemo-deployment-f668d8569-xphbx', namespace='default')
        pprint(status)
        return "test"

    except ApiException as e:
        print("Exception when calling CoreV1Api->list_pod_for_all_namespaces: %s\n" % e)