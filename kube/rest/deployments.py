#!/usr/local/miniconda2/bin/python
# _*_ coding:utf-8 _*_
"""
# @Time   : 2018/7/20 17:59
# @Author : 张城城
"""
from flask import Blueprint, jsonify, request
from kubernetes import client
from kube.rest import configKube as conf
from kubernetes.client.rest import ApiException
from pprint import pprint

deploy = Blueprint('deployments', __name__)


@deploy.route('/update')
def update_deployment():
    extension = conf.get_extensions()


@deploy.route('/getDeployList')
def get_deployment():
    extension = conf.get_extensions()
    return_model = {}
    deploy_list = []
    try:
        deploy = extension.list_deployment_for_all_namespaces()
        pprint(deploy)
        for i in deploy.items:
            #print i.metadata.name
            name = i.metadata.name
            create_time = i.metadata.creation_timestamp
            namespace = i.metadata.namespace
            expect_replicas = i.spec.replicas
            available_replicas = i.status.available_replicas
            if available_replicas is None:
                available_replicas = 0
            image = i.spec.template.spec.containers[0].image
            print create_time
            temp = {'name': name, 'namespace': namespace, 'expect_replicas': expect_replicas,
                     'available_replicas': available_replicas, 'create_time': create_time, 'image': image}
            deploy_list.append(temp)

        return_model['retCode'] = 200
        return_model['retDesc'] = 'success'
        return_model['data'] = deploy_list
    except ApiException as e:
        return_model['retCode'] = 500
        return_model['retDesc'] = 'fail'
        return_model['data'] = None
        print e

    return jsonify(return_model)


@deploy.route('/create')
def create_deployment():
    """
    创建deployment
    :return:
    """
    return_model = {}
    name = request.args.get('name', 'sweet_zcc')
    namespace = request.args.get('namespace', 'default')    # 命名空间

    replicas = request.args.get('replicas', 1)  # 副本的数量
    image = request.args.get("image")   # 镜像名称
    container_port = request.args.get("containerPort")  # 容器的端口
    deployment = client.ExtensionsV1beta1Deployment()

    """
    填充 Deployment fields: apiVersion, kind, metadata
    """
    deployment_labels = request.args.get('deploymentLabels')    # Deployment的标签
    deployment_name = request.args.get('deploymentName')        # Deployment的名称

    deployment.api_version = 'extensions/v1beta1'
    deployment.kind = 'Deployment'
    deployment.metadata = client.V1ObjectMeta(name=deployment_name, labels=deployment_labels)

    """
    填充 Deployment .spec字段
    """
    spec = client.ExtensionsV1beta1DeploymentSpec()
    spec.replicas = replicas
    """
    Deployment部署的 spec的template
    即 Add Pod template in .spec.template
    """
    pod_labels = request.args.get("podLabels")  # pod的标签
    spec.template = client.V1PodTemplateSpec()
    spec.template.metadata = client.V1ObjectMeta(labels=pod_labels)
    spec.template.spec = client.V1PodSpec()

    """
    Pod template container description
    """
    container = client.V1Container()
    container.name = name  # 名称
    container.image = image  # 镜像名称
    protocol = request.args.get('protocol')
    ports = client.V1ContainerPort(container_port=container_port)
    if protocol:
        ports.protocol = protocol
    container.ports = [ports]

    spec.template.spec.containers = [container]
    deployment.spec = spec
    try:
        extension = conf.get_extensions()
        extension.create_namespaced_deployment(namespace=namespace, body=deployment)
        return_model['retDesc'] = 'success'
        return_model['retCode'] = 200
        return_model['data'] = None
    except ApiException as e:
        return_model['retCode'] = 500
        return_model['retDesc'] = 'fail'
        return_model['data'] = None
        print e

    return jsonify(return_model)


