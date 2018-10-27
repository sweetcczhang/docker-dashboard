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
from kube import service
from kube import deploy
from kube import file_create
from harbor.rest import harbor as harbor_client
from werkzeug.utils import secure_filename
import os
from yamls_location_config import YAML_LOC
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


@hosts.route('/getClusterInfo', methods=['GET', 'POST'])
def get_all_cluster_info():
    return_model = {}
    pod_list = pods.get_all_pods()
    deploy_list = deploy.get_all_deployment()
    service_list = service.get_service_info()
    node_list = hostInfo.get_host_info()
    repositories = harbor_client.repositories.list(1)
    data = {
        'hosts': {
            'hostNum': node_list[0],
            'readyNum': node_list[2],
            'notReadyNum': node_list[3]
        },
        'pods': {
            'readyNum': pod_list[0],
            'notReadyNum': 0
        },
        'deployNum': deploy_list[0],
        'serviceNum': service_list[0],
        'repoNum': len(repositories)
    }
    return_model['retCode'] = 200
    return_model['retDesc'] = 'success'
    return_model['data'] = data
    return jsonify(return_model)


@hosts.route('/yaml', methods=['GET', 'POST'])
def upload_file():
    return_model = {}
    try:
        if request.method == 'POST':
            files = request.files['file']
            filename = secure_filename(files.filename)
            file_path = os.path.join(YAML_LOC, filename)
            if os.path.exists(file_path):
                os.remove(file_path)
            files.save(file_path)
            if filename.rsplit('.', 1)[1] == 'json':
                file_create.create_from_json(json_name=filename)
            elif filename.rsplit('.', 1)[1] == 'yaml':
                file_create.create_from_yaml(filename)
            return_model['retCode'] = 200
            return_model['retDesc'] = 'success'
            return_model['data'] = None
        else:
            raise Exception('请求方法错误')
    except Exception as e:
        return_model['retCode'] = 500
        return_model['retDesc'] = '创建任务失败'
        print e



