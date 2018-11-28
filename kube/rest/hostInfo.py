#!/usr/local/miniconda2/bin/python
# _*_ coding:utf-8 _*_
"""
#
# @Time   : 2018/7/21 15:37
# @Author : 张城城
"""
from flask import Blueprint, jsonify, request

from kube import hostInfo
from kube import pods_client
from kube import service_client
from kube import deploys
from kube import file_create
from harbor.rest import harbor as harbor_client
from werkzeug.utils import secure_filename
import os
from yamls_location_config import YAML_LOC
import json
hosts = Blueprint('hostInfo', __name__)


@hosts.route('/getHostList', methods=['GET', 'POST'])
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


@hosts.route('/search', methods=['GET', 'POST'])
def search():
    return_model = {}
    host_name = request.values.get(key='hostName')
    try:
        host_detail = hostInfo.get_host_by_hostname(host_name=host_name)
        return_model['retCode'] = 200
        return_model['retDesc'] = 'success'
        return_model['data'] = [host_detail]
    except Exception as e:
        print e
        return_model['retCode'] = 500
        return_model['retDesc'] = '查询%s主机失败', host_name
    return jsonify(return_model)


@hosts.route('/getHostDetail', methods=['GET', 'POST'])
def get_host_detail():
    """
    获取主机详细信息
    :return:
    """
    return_model = {}
    host_name = request.values.get(key='hostName', default=None)
    try:
        host_detail = hostInfo.host_detail(host_name=host_name)
        pod_info = pods_client.get_pod_from_label_or_field(field_selector=host_name)
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
    return jsonify(return_model)


@hosts.route('/getClusterInfo', methods=['GET', 'POST'])
def get_all_cluster_info():
    return_model = {}
    pod_list = pods_client.get_all_pods()
    deploy_list = deploys.get_all_deployment()
    service_list = service_client.get_service_info()
    node_list = hostInfo.get_host_info()
    repositories = harbor_client.repositories.list(1)
    not_ready = 0
    for pod in pod_list[1]:
        if pod['status'] == 'Pending':
            not_ready += 1

    data = {
        'hosts': {
            'totalNum': node_list[0],
            'readyNum': node_list[2],
            'notReadyNum': node_list[3]
        },
        'pods': {
            'totalNum': pod_list[0],
            'readyNum': pod_list[0]-not_ready,
            'notReadyNum': not_ready,
        },
        'deployNum': deploy_list[0],
        'serviceNum': service_list[0],
        'repoNum': len(repositories),
        'logNum': 15
    }
    return_model['retCode'] = 200
    return_model['retDesc'] = 'success'
    return_model['data'] = data
    return jsonify(return_model)


@hosts.route('/yaml', methods=['GET', 'POST'])
def upload_file():
    """
    通过上传的json文件或者yaml文件创建应用
    :return:
    """
    return_model = {}
    print 'test'
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

    return jsonify(return_model)


@hosts.route('/getJson', methods=['POST', 'GET'])
def get_json_from_value():
    return_model = {}
    jsons = request.values.get(key='json', deploys=None)
    if jsons is None:
        return_model['retCode'] = 500
        return_model['retDesc'] = 'json参数不能为空'
    try:
        file_create.get_json(jsons)
        return_model['retCode'] = 200
        return_model['retDesc'] = 'success'
    except Exception as e:
        print e
        return_model['retCode'] = 500
        return_model['retDesc'] = '请检查json参数格式是否正确'
    return jsonify(return_model)


@hosts.route('/getYaml', methods=['POST', 'GET'])
def get_yaml_from_value():

    return_model = {}
    yaml_value = request.values.get(key='yaml', default=None)
    if yaml_value is None:
        return_model['retCode'] = 500
        return_model['retDesc'] = 'yaml参数不能为空'
    try:
        file_create.get_yaml(f=yaml_value)
        return_model['retCode'] = 200
        return_model['retDesc'] = 'success'
    except Exception as e:
        print e
        return_model['retCode'] = 500
        return_model['retDesc'] = '请检查yaml文件的格式是否正确'
    return return_model


@hosts.route('/labelHost', methods=['POST', 'GET'])
def label_host():
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
            commands = 'kubectl label host ' + name + la
            output = os.popen(commands)
            result = request + output.read()
        return_model['retCode'] = 200
        return_model['retDesc'] = 'success'
        return_model['data'] = result
    except Exception as e:
        print e
        return_model['retCode'] = 500
        return_model['retDesc'] = 'host打标签失败'

    return jsonify(return_model)