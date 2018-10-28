#!/usr/local/miniconda2/bin/python
# _*_ coding:utf-8 _*_
"""
# @Time   : 2018/7/11 23:49
# @Author : 张城城
"""
from flask import Blueprint, jsonify,request
from kubernetes.client.rest import ApiException
from kube.rest import configKube as conf

sevices = Blueprint('services', __name__)


@sevices.route('/create_service')
def create_service():
    v1 = conf.get_core_v1_api()
    return_model = {}
    #name = request.args.get('name')
    #namespace = request.args.get('namespace', 'default')
    name = 'example-service'
    namespace = 'default'
    try:
        api_response = v1.read_namespaced_service(name=name, namespace=namespace)
        return_model['retCode'] = 200
        return_model['retDesc'] = 'success'
        return_model['data'] = api_response
        print return_model
    except ApiException as e:
        return_model['retCode'] = 500
        return_model['retDesc'] = 'failure'
        return_model['data'] = None
        print e




@sevices.route('/get_service_detail')
def get_service_details():
    """
    获取某个service的具体信息内容
    :return:
    """
    v1 = conf.get_core_v1_api()


@sevices.route('/get_service_by_namespace')
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


@sevices.route('/get_services')
def get_service_info():
    """
    获取集群中所有的service的信息
    :return:
    """
    v1 = conf.get_core_v1_api()
    return_model = {}
    lists =[]
    try:
        sevices_list = v1.list_service_for_all_namespaces().items
        for i in sevices_list:
            name = i.metadata.name
            namespace = i.metadata.namespace
            label = i.metadata.labels
            labels = ''
            for key, value in label.items():
                labels = labels + key + '=' + value + ','
            labels = labels.encode('utf-8')
            cluster_ip = i.spec.cluster_ip
            hello = i.spec.type
            ports = i.spec.ports[0]
            port = ''
            if ports.node_port != 'None':
                port = str(ports.node_port) + ':'
            port = port + str(ports.port) + "/TCP"

            temp ={"name": name, "namespace": namespace, "labels": labels,
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


if __name__ == "__main__":
    create_service()
    #get_service_info()