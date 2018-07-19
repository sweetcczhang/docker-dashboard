#!/usr/local/miniconda2/bin/python
# _*_ coding:utf-8 _*_
"""
# @Time   : 2018/7/11 23:49
# @Author : 张城城
"""
from flask import Blueprint, jsonify
from kubernetes import client, config
from kubernetes.client.rest import ApiException
from pprint import pprint

pods = Blueprint('kube', __name__)


def config1():
    config.load_kube_config(config_file='/root/zcc/hello/config')
    v1 = client.CoreV1Api()
    return v1


@pods.route('/test')
def get_all_pods():

    v1 = config1()
    print ("Listing pods with their ips:")
    try:
        ret = v1.list_pod_for_all_namespaces()
        re = v1.list_node()
        pprint(ret)
        list = []
        for i in ret.items:
            print("%s\t%s\t%s\t%s" % (i.metadata.name, i.metadata.namespace, i.status.host_ip, i.status.pod_ip))
            temp = {'name': i.metadata.name, 'namespace': i.metadata.namespace, 'host_ip': i.status.host_ip,
                    'pod_ip': i.status.pod_ip}
            list.append(temp)
        return jsonify({'pods': list})
    except ApiException as e:
        print("Exception when calling CoreV1Api->list_pod_for_all_namespaces: %s\n" % e)


@pods.route('/resource')
def get_namespaced_pod_log( name, namespace='default'):

    v1 = config1()
    print ("Listing pods with their ips:")
    try:
        resouce = v1.read_namespaced_pod_log(name=name,namespace=namespace)
        pprint(resouce)
        return resouce
    except ApiException as e:
        print("Exception when calling CoreV1Api->list_pod_for_all_namespaces: %s\n" % e)


@pods.route('/status')
def get_namespace_pod_status():

    v1 = config1()
    try:
        status = v1.read_namespaced_pod_status(name='nodedemo-deployment-f668d8569-xphbx', namespace='default')
        pprint(status)
        return "test"

    except ApiException as e:
        print("Exception when calling CoreV1Api->list_pod_for_all_namespaces: %s\n" % e)