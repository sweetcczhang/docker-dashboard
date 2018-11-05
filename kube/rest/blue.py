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
from kube import pods_client
from kube import name_space
pods = Blueprint('kube', __name__)


def config1():
    config.load_kube_config(config_file='/root/zcc/hello/config')
    v1 = client.CoreV1Api()
    return v1


@pods.route('/listPods', methods=['GET', 'POST'])
def get_all_pods():
    """
    获取pod List的信息
    :return:
    """
    return_model = {}
    namespace = request.values.get(key='namespace', default=None)
    print ("Listing pods with their ips:")
    try:
        pod_info = pods_client.get_all_pods(namespace=namespace)

        data = {'length': pod_info[0], 'podsList': pod_info[1]}

        return_model['data'] = data
        return_model['retCode'] = 200
        return_model['retDesc'] = 'success'
    except Exception as e:
        print("Exception when calling CoreV1Api->list_pod_for_all_namespaces: %s\n" % e)
        return_model['retCode'] = 500
        return_model['retDesc'] = '获取pod List信息失败'
    return jsonify(return_model)


@pods.route('/createPods', methods=['GET', 'POST'])
def create_pod():
    return_model = {}
    name = request.values.get(key='name', default=None)
    image = request.values.get(key='image', default=None)
    labels = request.values.get(key='labels', default=None)
    namespace = request.values.get(key='namespace', default='default')
    ports = request.values.get(key='ports', default=None)
    args = request.values.get(key='args', default=None)
    commands = request.values.get(key='commands', default=None)
    hostname = request.values.get(key='hostname', default=None)
    limits = request.values.get(key='limits', default=None)
    requests = request.values.get(key='requests', default=None)
    if name is None or image is None:
        return_model['retCode'] = 500
        return_model['retDesc'] = 'name或者iamge不能为空'
    try:
        result = pods_client.create_pod(name=name, image=image, labels=labels, namespace=namespace, ports=ports,
                                        commands=commands, args=args, hostname=hostname, limits=limits, requests=requests)
        if result:
            return_model['retCode'] = 200
            return_model['retDesc'] = 'success'
        else:
            raise Exception("创建pod失败")
    except Exception as e:
        return_model['retCode'] = 500
        return_model['retDesc'] = '创建pod失败'
        print e
    return jsonify(return_model)


@pods.route('/getPodsFromLabel', methods=['GET', 'POST'])
def get_pods_from_field_or_label():
    """
    通过label selector或者 field selector获取pods
    :return:
    """
    return_model = {}
    field_selector = request.values.get(key='fieldSelector', default=None)
    label_selector = request.values.get(key='labelSelector', default=None)
    namespace = request.values.get(key='namespace', default='default')
    if field_selector is None and label_selector is None:
        return_model['retCode'] = 500
        return_model['retDesc'] = 'fieldSelector和labelSelector不能同时为空'
        return jsonify(return_model)
    try:
        pods_info = pods_client.get_pod_from_label_or_field(field_selector=field_selector,namespace=namespace,
                                                            label_selector=label_selector)
        data = {'length': pods_info[0], 'podsList': pods_info[1]}
        return_model['retCode'] = 200
        return_model['retDesc'] = 'success'
        return_model['data'] = data
    except Exception as e:
        print e
        return_model['retCode'] = 500
        return_model['retDesc'] = '请检查参数是否正确'
    return jsonify(return_model)


@pods.route('/getPodDetail', methods=['GET', 'POST'])
def get_pod_detail():
    return_model = {}
    name = request.values.get(key='name', default=None)
    namespace = request.values.get(key='namespace', default='default')
    if name is None:
        return_model['retCode'] = 500
        return_model['retDesc'] = 'pod 名称不能为空'
        return jsonify(return_model)
    try:
        pod_info = pods_client.get_pod_details(name=name, namespace=namespace)
        return_model['retCode'] = 200
        return_model['retDesc'] = 'success'
        return_model['data'] = pod_info
    except Exception as e:
        print e
        return_model['retCode'] = 500
        return_model['retDesc'] = '请检查pod名称是否正确'

    return jsonify(return_model)


@pods.route('/getPodLog')
def get_namespaced_pod_log():
    """
    :return:
    """
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


@pods.route('/getAllNamespaces', methods=['GET', 'POST'])
def get_all_namespaces():
    return_model = {}
    try:
        result = name_space.list_all_namespace()
        return_model['retCode'] = 200
        return_model['retDesc'] = 'success'
        return_model['data'] = {'length': len(result),'namespaceList': result}
    except Exception as e:
        print e
        return_model['retCode'] = 500
        return_model['retDesc'] = '获取namespace列表失败'

    return jsonify(return_model)
