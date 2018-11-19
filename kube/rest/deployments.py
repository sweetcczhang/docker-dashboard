#!/usr/local/miniconda2/bin/python
# _*_ coding:utf-8 _*_
"""
# @Time   : 2018/7/20 17:59
# @Author : 张城城
"""
from flask import Blueprint, jsonify, request
from kube import deploys
from kube import service_client
from kube import scale_client
from kube import pods_client

deploy = Blueprint('deployments', __name__)


@deploy.route('/updateDeployment', methods=['GET', 'POST'])
def update_deployment():
    return_model = {}
    name = request.values.get(key='name')  # deployment的名称
    namespace = request.values.get(key='namespace', default='default')  # 命名空间

    replicas = request.values.get(key='replicas', default=1)  # 副本的数量
    image = request.values.get(key='image', default=None)  # 镜像名称
    # container_port = request.args.get("containerPort")  # 容器的端口
    labels = request.values.get(key='labels', default=None)  # deployment标签

    container_name = request.values.get(key='containerName', default=name)  # 容器的名称
    ports = request.values.get(key='ports', default=None)  # 容器的端口
    template_labels = request.values.get(key='templateLabels', default=labels)  # templateLabels
    resources = request.values.get(key='resources', default=None)  # 资源限制
    commands = request.values.get(key='commands', default=None)
    args = request.values.get('args')


@deploy.route('getDeployDetail', methods=['GET', 'POST'])
def get_deployment_detail():
    return_model = {}
    namespace = request.values.get(key='namespace', default='default')
    name = request.values.get(key='name', default=None)
    if name is None:
        return_model['retCode'] = 500
        return_model['retDesc'] = '参数错误，name不能为空'
        return jsonify(return_model)
    try:
        deployment = deploys.get_deployment_detail(name=name, namespace=namespace)

        label_select = deployment['selectors']
        label = []
        for key, value in label_select.items():
            temp = key + '=' + value
            label.append(temp)

        pod_list = pods_client.get_pod_from_label_or_field(label_selector=label[0], namespace=namespace)

        serivce_detail = service_client.get_service_from_label_selector(label_selector=label[0], namespace=namespace)

        auto_scale = scale_client.get_auto_scaling_detail(name=name, namespace=namespace)

        data = {
            'deployment': deployment,
            'podList': pod_list,
            'service': serivce_detail,
            'autoScale': auto_scale
        }
        return_model['retCode'] = 200
        return_model['retDesc'] = 'success'
        return_model['data'] = data
    except Exception as e:
        return_model['retCode'] = 500
        return_model['retDesc'] = '请检查参数是否正确'
        print e
    return jsonify(return_model)


@deploy.route('/getDeployList', methods=['GET', 'POST'])
def get_deployment():
    namespace = request.values.get('namespace', None)
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
    name = request.values.get(key='name', default=None)
    namespace = request.values.get(key='namespace', default='default')
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
    """
    first part
    """
    name = request.values.get(key='name')   # deployment的名称
    print 'name:' + name

    namespace = request.values.get(key='namespace', default='default')    # 命名空间
    print 'namespace:' + namespace
    replicas = int(request.values.get(key='replicas', default=1))  # 副本的数量
    print 'replicas: %d', replicas

    image = request.values.get(key='image', default=None)   # 镜像名称
    print 'image:' + image
    host_name = request.values.get(key='hostName', default=None)
    if host_name == '':
        host_name = None
    print 'hostName:'
    print host_name
    cpu = request.values.get(key='cpu', default=None)
    print "cpu:" + cpu
    memory = request.values.get(key='memory')
    print "memory:" + memory
    log = request.values.get(key='log')
    print 'log:' + log
    labels = request.values.get(key='labels', default=None)  # deployment标签
    print 'labels:'
    print labels
    labels = labels.encode('utf-8')
    is_start = request.values.get(key='isStart')
    print 'is_start:' + is_start

    """
    second part
    """
    container_port = request.values.get("containerPort")  # 容器的端口
    container_port = container_port.encode('utf-8')
    print 'container_port:'
    print container_port
    volumn = request.values.get(key='volumn', default=None)
    volumn = volumn.encode('utf-8')
    print 'volumn:'
    print volumn

    """
    third part
    """
    commands = request.values.get(key='commands', default=None)
    print 'commands:'
    print commands
    env = request.values.get(key='env', default=None)
    env = env.encode('utf-8')
    print 'env:'
    print env
    args = request.values.get(key='args', default=None)
    print 'args:'
    print args

    """
    fourth part
    """
    is_service = request.values.get(key='isService', default='true')
    print 'is_service:'
    print is_service
    if is_service == 'true':
        port_type = request.values.get(key='portType', default='NodePort')
        print 'port_type:'
        print port_type
        service_port = request.values.get(key='servicePort')
        print 'service_port:'
        print service_port

    """
    fifth part
    """
    is_auto = request.values.get(key='isAuto', default='true')
    print 'is_auto:'
    print is_auto

    if is_auto == 'true':

        min_replicas = int(request.values.get(key='min', default=1))
        print 'min_replicas:'
        print min_replicas

        max_replicas = int(request.values.get(key='max', default=10))
        print 'max_replicas'
        print max_replicas

        auto_cpu = int(request.values.get(key='autoCpu', default=100))
        print 'auto_cpu'
        print auto_cpu

        auto_memory = int(request.values.get(key='autoMemory', default=100))
        print 'auto_memory'
        print auto_memory

        customer = request.values.get(key='customer', default=None)

        if customer == '':
            customer = None
        elif customer == '[]':
            customer = None

        print 'customer:'
        print customer

    if image is None:
        return_model['retCode'] = 500
        return_model['retDesc'] = '参数错误，镜像不能为空'
        return jsonify(return_model)
    deployment = deploys.create_deployment_yaml(name=name, image=image, namespace=namespace, labels=labels,
                                                container_name=name, ports=container_port,
                                                template_labels=labels,
                                                replicas=replicas, cpu=cpu, memory=memory, commands=commands, args=args,
                                                env=env)
    try:
        # result = deploys.create_deployment(deployment=deployment, namespace=namespace)
        result = False
        if is_service == 'true':
            service_client.create_service(name=name, labels=labels, namespace=namespace, port_type=port_type,
                                          s_port=service_port, selectors=labels)
        if is_auto == 'true':
            scale_client.create_auto_scale(namespace=namespace, name=name, labels=labels, deploy_name=name,
                                           min_replicas=min_replicas, max_replicas=max_replicas, cpu=auto_cpu,
                                           memory=auto_memory, customer=customer)
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



