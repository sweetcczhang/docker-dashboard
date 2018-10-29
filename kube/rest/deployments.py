#!/usr/local/miniconda2/bin/python
# _*_ coding:utf-8 _*_
"""
# @Time   : 2018/7/20 17:59
# @Author : 张城城
"""
from flask import Blueprint, jsonify, request
from kubernetes import client
from kubernetes.client.rest import ApiException
from pprint import pprint
from kube import deploys
from kube.rest import configKube as conf

deploy = Blueprint('deployments', __name__)


@deploy.route('/updateDeployment')
def update_deployment():
    return_model = {}
    name = request.args.get(key='name')  # deployment的名称
    namespace = request.args.get(key='namespace', default='default')  # 命名空间

    replicas = request.args.get(key='replicas', default=1)  # 副本的数量
    image = request.args.get(key='image', default=None)  # 镜像名称
    # container_port = request.args.get("containerPort")  # 容器的端口
    labels = request.args.get(key='labels', default=None)  # deployment标签

    container_name = request.args.get(key='containerName', default=name)  # 容器的名称
    ports = request.args.get(key='ports', default=None)  # 容器的端口
    template_labels = request.args.get(key='templateLabels', default=labels)  # templateLabels
    resources = request.args.get(key='resources', default=None)  # 资源限制
    commands = request.args.get(key='commands', default=None)
    args = request.args.get('args')



@deploy.route('getDeployDetail', methods=['GET', 'POST'])
def get_deployment_detail():
    return_model = {}
    namespace = request.args.get(key='namespace', default='default')
    name = request.args.get(key='name', default=None)
    if name is None:
        return_model['retCode'] = 500
        return_model['retDesc'] = '参数错误，name不能为空'
        return jsonify(return_model)
    try:
        deployment = deploys.get_deployment_detail(name=name, namespace=namespace)
        return_model['retCode'] = 200
        return_model['retDesc'] = 'success'
        return_model['data'] = deployment
    except Exception as e:
        return_model['retCode'] = 500
        return_model['retDesc'] = '请检查参数是否正确'
        print e
    return jsonify(return_model)


@deploy.route('/getDeployList', methods=['GET', 'POST'])
def get_deployment():
    namespace = request.args.get('namespace', None)
    return_model = {}
    try:
        deployment = deploys.get_all_deployment(namespace=namespace)
        data = {'length': deployment[0], 'deployments': deployment[1]}
        return_model['retCode'] = 200
        return_model['retDesc'] = 'success'
        return_model['data'] = data
    except Exception as e:
        return_model['retCode'] = 500
        return_model['retDesc'] = 'fail'
        return_model['data'] = None
        print e
    return jsonify(return_model)


@deploy.route('/deleteDeployment', methods=['GET', 'POST'])
def delete_deployment():
    return_model = {}
    name = request.args.get(key='name', default=None)
    namespace = request.args.get(key='namespace', default='default')
    try:
        if name is None:
            raise Exception('参数name不能为空')
        result = deploys.delete_deployment(name=name, namespace=namespace)
        if result:
            return_model['retCode'] = 200
            return_model['retDesc'] = 'success'
        else:
            raise Exception('删除deployment %s', name)
    except Exception as e:
        return_model['retCode'] = 500
        return_model['retDesc'] = e.message
        print e
    return jsonify(return_model)


@deploy.route('/create', methods=['GET', 'POST'])
def create_deployment():
    """
    创建deployment
    :return:
    """
    return_model = {}
    name = request.args.get(key='name')   # deployment的名称
    namespace = request.args.get(key='namespace', default='default')    # 命名空间

    replicas = request.args.get(key='replicas', default=1)  # 副本的数量
    image = request.args.get(key='image', default=None)   # 镜像名称
    # container_port = request.args.get("containerPort")  # 容器的端口
    labels = request.args.get(key='labels', default=None)  # deployment标签

    container_name = request.args.get(key='containerName', default=name)    # 容器的名称
    ports = request.args.get(key='ports', default=None)  # 容器的端口
    template_labels = request.args.get(key='templateLabels', default=labels)    # templateLabels
    resources = request.args.get(key='resources', default=None)  # 资源限制
    commands = request.args.get(key='commands', default=None)
    args = request.args.get('args')

    if image is None:
        return_model['retCode'] = 500
        return_model['retDesc'] = '参数错误，镜像不能为空'
        return jsonify(return_model)
    deployment = deploys.create_deployment_yaml(name=name, image=image, namespace=namespace, labels=labels,
                                   container_name=container_name, ports=ports, template_labels=template_labels,
                                   replicas=replicas, resources=resources, commands=commands, args=args)
    try:
        result = deploys.create_deployment(deployment=deployment, namespace=namespace)
        if result:
            return_model['retCode'] = 200
            return_model['retDesc'] = 'success'
        else:
            raise Exception('创建deployment失败')
    except Exception as e:
        return_model['retCode'] = 500
        return_model['retDesc'] = '请检查参数'
        print e
    return jsonify(return_model)

    # deployment = client.ExtensionsV1beta1Deployment()
    # """
    # 填充 Deployment fields: apiVersion, kind, metadata
    # """
    # deployment_labels = request.args.get('deploymentLabels')    # Deployment的标签
    # deployment_name = request.args.get('deploymentName')        # Deployment的名称
    #
    # deployment.api_version = 'extensions/v1beta1'
    # deployment.kind = 'Deployment'
    # deployment.metadata = client.V1ObjectMeta(name=deployment_name, labels=deployment_labels)
    #
    # """
    # 填充 Deployment .spec字段
    # """
    # spec = client.ExtensionsV1beta1DeploymentSpec()
    # spec.replicas = replicas
    # """
    # Deployment部署的 spec的template
    # 即 Add Pod template in .spec.template
    # """
    # pod_labels = request.args.get("podLabels")  # pod的标签
    # spec.template = client.V1PodTemplateSpec()
    # spec.template.metadata = client.V1ObjectMeta(labels=pod_labels)
    # spec.template.spec = client.V1PodSpec()
    #
    # """
    # Pod template container description
    # """
    # container = client.V1Container()
    # container.name = name  # 名称
    # container.image = image  # 镜像名称
    # protocol = request.args.get('protocol')
    # ports = client.V1ContainerPort(container_port=container_port)
    # if protocol:
    #     ports.protocol = protocol
    # container.ports = [ports]
    #
    # spec.template.spec.containers = [container]
    # deployment.spec = spec
    # try:
    #     extension = conf.get_extensions()
    #     extension.create_namespaced_deployment(namespace=namespace, body=deployment)
    #     return_model['retDesc'] = 'success'
    #     return_model['retCode'] = 200
    #     return_model['data'] = None
    # except ApiException as e:
    #     return_model['retCode'] = 500
    #     return_model['retDesc'] = 'fail'
    #     return_model['data'] = None
    #     print e



