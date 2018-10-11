#!/usr/local/miniconda2/bin/python
# _*_ coding:utf-8 _*_
"""
#
# @Time   : 2018/7/21 15:37
# @Author : 张城城
"""
from flask import Blueprint, jsonify
from kubernetes.client.rest import ApiException
from kube import configKube as conf
hosts = Blueprint('hostInfo', __name__)


@hosts.route('/getHostList')
def get_host_info():
    """
    获取主机列表信息
    :return:
    """
    v1 = conf.get_core_v1_api()
    return_model = {}
    node_list = []
    try:
        host = v1.list_node()
        for i in host.items:
            s = str(i.metadata.creation_timestamp)
            create_time = s[:len(s)-6]
            name = i.metadata.name
            host_ip = i.spec.external_id
            status = 'NotReady'
            os = i.status.node_info.os_image
            docker_version = i.status.node_info.container_runtime_version
            cpu = i.status.capacity[u'cpu']
            memory = i.status.capacity[u'memory']
            memory = memory[:len(memory)-2]
            memory = int(memory)/1024
            memory = str(memory)+'Mi'
            status_1 = i.status.conditions[-1].status
            print status_1
            if status_1 == 'True':
                status = 'Ready'
            temp = {'name': name, 'hostIp': host_ip, 'status': status, 'os': os, 'dockerVersion': docker_version,
                    'cpu': cpu, 'memory': memory, 'createTime': create_time}
            node_list.append(temp)

        return_model['retCode'] = 200
        return_model['retDesc'] = 'success'
        return_model['data'] = node_list

    except ApiException as e:
        return_model['retCode'] = 500
        return_model['retDesc'] = '获取消息失败'
        return_model['data'] = None
        print("Exception when calling CoreV1Api->list_node: %s\n" % e)
    return jsonify(return_model)
