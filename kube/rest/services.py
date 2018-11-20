#!/usr/local/miniconda2/bin/python
# _*_ coding:utf-8 _*_
"""
# @Time   : 2018/7/11 23:49
# @Author : 张城城
"""
from flask import Blueprint, jsonify,request
from kubernetes.client.rest import ApiException
from kube.rest import configKube as conf
from kube import service_client
from kube import pods_client
import json
import os

service_s = Blueprint('services', __name__)


@service_s.route('/createService', methods=['GET', 'POST'])
def create_service():
    return_model = {}
    serivce_data = request.values.get('serviceData', 'zcc')
    print 'serivce_data:' + serivce_data
    name = request.values.get(key='name')
    print name
    namespace = request.values.get(key='namespace', default='default')
    print namespace
    labels = request.values.get(key='labels', default=None)
    labels = labels.encode('utf-8')
    port_type = request.values.get(key='portType', default=None)
    v_port = request.values.get(key='ports', default=None)
    v_port = v_port.encode('utf-8')
    selector = request.values.get(key='selector', default=None)
    selector = selector.encode('utf-8')
    selector = [selector]
    print labels
    print v_port
    print selector

    try:
        service_client.create_service(name=name, labels=labels, namespace=namespace, port_type=port_type,
                                      s_port=v_port, selectors=selector)
        return_model['retCode'] = 200
        return_model['retDesc'] = 'success'
        print return_model
    except ApiException as e:
        return_model['retCode'] = 500
        return_model['retDesc'] = '创建service失败'
        print e
    return jsonify(return_model)


@service_s.route('/get_service_detail', methods=['GET', 'POST'])
def get_service_details():
    """
    获取某个service的具体信息内容
    :return:
    """
    return_model = {}
    name = request.values.get(key='name', default=None)
    namespace = request.values.get(key='namespace', default='default')
    try:
        service_detail = service_client.get_service_detail(name=name, namespace=namespace)
        labels = service_detail['selectors']
        labels = labels.split(',')
        pods_list = pods_client.get_pod_from_label_or_field(label_selector=labels[0], namespace=namespace)
        return_model['retCode'] = 200
        return_model['retDesc'] = 'success'
        return_model['data'] = service_detail
    except Exception as e:
        print e
        return_model['retCode'] = 500
        return_model['retDesc'] = '查询service详细信息失败'
    return jsonify(return_model)


@service_s.route('/getServices/fromFieldOrLabel', methods=['GET', 'POST'])
def get_service_from_field_label():
    label_selector = request.values.get(key='label_selector', default=None)
    namespace = request.values.get(key='namespace', default='default')
    return_model = {}
    try:
        services_list = service_client.get_service_from_label_selector(label_selector=label_selector, namespace=namespace)
        data = {'length': services_list[0], 'servicesList': services_list[1]}
        return_model['retCode'] = 200
        return_model['retDesc'] = 'success'
        return_model['data'] = data
    except Exception as e:
        return_model['retDesc'] = '通过label查询service失败'
        return_model['retCode'] = 500
        print e
    return jsonify(return_model)


@service_s.route('/get_service_by_namespace', methods=['GET', 'POST'])
def get_service_by_namespace():
    """
    获取某个命名空间中所有的服务
    :return:
    """
    v1 = conf.get_core_v1_api()
    return_model = {}
    lists = []
    namespace = request.args.get("namespace", "default")

    try:
        api_response = v1.list_namespaced_service(namespace=namespace).items
        for svc in api_response:
            name = svc.metadata.name
            namespace = svc.metadata.namespace
            label = svc.metadata.labels
            labels = ''
            for key, value in label.items():
                labels = labels + key + '=' + value + ','
            labels = labels.encode('utf-8')
            cluster_ip = svc.spec.cluster_ip
            hello = svc.spec.type
            ports = svc.spec.ports[0]
            port = ''
            s = ports.node_port
            if s != 'None':
                port = str(ports.node_port) + ':'
            port = port + str(ports.port) + "/TCP"

            temp = {"name": name, "namespace": namespace, "labels": labels,
                    "cluster_ip": cluster_ip, "type": hello, "port": port}
            print temp
            lists.append(temp)
        return_model['retCode'] = 200
        return_model['retDesc'] = 'success'
        return_model['data'] = lists

    except ApiException as e:
        return_model['retCode'] = 500
        return_model['retDesc'] = 'failure'
        return_model['data'] = None
        print e

    return jsonify(return_model)


@service_s.route('/getServices', methods=['GET', 'POST'])
def get_service_info():
    """
    获取集群中所有的service的信息
    :return:
    """
    return_model = {}
    namespace = request.values.get(key='namespace', default=None)
    try:
        services_list = service_client.get_service_info(namespace=namespace)
        data = {'length': services_list[0], 'servicesList': services_list[1]}
        return_model['retCode'] = 200
        return_model['retDesc'] = 'success'
        return_model['data'] = data

    except Exception as e:
        return_model['retCode'] = 500
        return_model['retDesc'] = 'failure'
        return_model['data'] = None
        print e
    return jsonify(return_model)


@service_s.route('/deleteService', methods=['GET', 'POST'])
def delete_service():
    return_model = {}
    name = request.values.get(key='name', default=None)
    namespace = request.values.get(key='namespace', default='default')
    try:
        result = service_client.delete_service(name=name, namespace=namespace)
        if result:
            return_model['retCode'] = 200
            return_model['retDesc'] = ('%s删除成功', name)
    except Exception as e:
        print e
        return_model['retCode'] = 500
        return_model['retDesc'] = ('%s删除失败', name)

    return jsonify(return_model)


@service_s.route('/labelService', methods=['GET', 'POST'])
def label_service():
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
            commands = 'kubectl label service ' + name + ' -n ' + namespace + la
            output = os.popen(commands)
            result = request + output.read()
        return_model['retCode'] = 200
        return_model['retDesc'] = 'success'
        return_model['data'] = result
    except Exception as e:
        print e
        return_model['retCode'] = 500
        return_model['retDesc'] = 'service打标签失败'

    return jsonify(return_model)


if __name__ == "__main__":
    # get_service_info()
    test = 'app=demo'
    print test.split(",")[0]