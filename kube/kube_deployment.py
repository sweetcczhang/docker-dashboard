#!/usr/local/miniconda2/bin/python
# _*_ coding:utf-8 _*_
"""
# @Project : docker-dashboard
# @Time    : 2018/10/13 下午2:35
# @Author  : zhangchengcheng
# @FileName: kube_deployment.py
# @Github  : https://github.com/sweetcczhang
"""
from kube import basic
from kubernetes.client.rest import ApiException
from datetime import datetime
import pytz
from kubernetes import client


class Deployments(basic.Client):

    def get_all_deployment(self, page=1, limit=10, namespace=None):
        """
        获取指定命名空间中所有的deployment或者所有命名空间中的deployment
        :param namespace:
        :return:
        """
        deploy_list = []
        try:
            if namespace is None:
                deploy = self.ext_client.list_deployment_for_all_namespaces(_continue=page, limit=limit)
            else:
                deploy = self.ext_client.list_namespaced_deployment(_continue=page, limit=limit, namespace=namespace)
            for i in deploy.items:
                # print i.metadata.name
                name = i.metadata.name
                create_time = i.metadata.creation_timestamp
                now_time = datetime.utcnow().replace(tzinfo=pytz.timezone("UTC"))
                days = (now_time - create_time).days
                create_time = str(create_time)
                create_time = create_time[:len(create_time)-6]
                namespace = i.metadata.namespace
                expect_replicas = i.spec.replicas
                available_replicas = i.status.available_replicas
                if available_replicas is None:
                    available_replicas = 0
                image = i.spec.template.spec.containers[0].image
                print create_time
                temp = {'name': name, 'namespace': namespace, 'expect_replicas': expect_replicas,
                        'available_replicas': available_replicas, 'create_time': create_time,
                        'image': image, 'days': days}
                deploy_list.append(temp)

        except ApiException as e:
            print e

        return deploy_list

    def get_deployment_detail(self, name, namespace='default'):
        """
        获取指定名称的部署(Deployment),用来展示其详细信息
        :param name:
        :param namespace:
        :return:
        """
        deploy = {}
        try:
            api_response = self.ext_client.read_namespaced_deployment(name=name, namespace=namespace)
            name = api_response.metadata.name
            labels = api_response.metadata.labels
            label = ''
            for key, value in labels.items():
                label = label + key.encode('utf-8') + ":" + value + ","
            label = label[:len(label)-1]
            create_time = api_response.metadata.creation_timestamp
            now_time = datetime.utcnow().replace(tzinfo=pytz.timezone("UTC"))
            days = (now_time - create_time).days
            create_time = str(create_time)
            create_time = create_time[:len(create_time) - 6]
            selectors = api_response.spec.selector.match_labels
            selector = ''
            for key, value in selectors.items():
                selector = selector + key.encode('utf-8') + ':' + value + ','
            selector = selector[:len(selector)-1]
            replica_set = api_response.status.conditions[1].message.split(" ")[1]
            replica_name = replica_set[1:len(replica_set)-1]
            replicas = api_response.spec.replicas
            replicas_available = api_response.status.available_replicas
            deploy = {'name': name, 'namespace': namespace, 'label': label, 'days': days,
                      'createTime': create_time, 'selector': selector, 'replicaName': replica_name,
                      'replicasNum': replicas, 'replicasAvailable': replicas_available}
            print deploy
        except ApiException as e:
            print e

        return deploy

    def create_deployment(self, deployment, namespace='default'):
        """
        创建一个deployment
        :param deployment: deployment的yaml文件
        :param namespace: deployment所在的命名空间
        :return:
        """
        try:
            #创建一个deployment
            api_response = self.ext_client.create_namespaced_deployment(namespace=namespace, body=deployment)
            print ("Deployment created. status='%s'" % str(api_response.status))
        except ApiException as e:
            print e

    def update_deployment(self, name, deployment, namespace='default'):
        """
        更新一个deployment
        :param name: deployment的名称
        :param deployment: deployment的名称
        :param namespace: deployment的命名空间
        :return:
        """
        try:
            api_response = self.ext_client.patch_namespaced_deployment(name=name,namespace=namespace,body=deployment)
            print ("Deployment updated. status='%s'" % str(api_response.status))
        except ApiException as e:
            print e

    def delete_deployment(self, name, namespace='default'):

        try:
            api_response = self.ext_client.delete_namespaced_deployment(name=name,
                                                                        namespace=namespace,
                                                                        body=client.V1DeleteOptions(propagation_policy='Foreground',
                                                                                                    grace_period_seconds=5))
            print ("Deployment deleted. status='%s'" % str(api_response.status))
        except ApiException as e:
            print e

    def create_deployment_yaml(self, name, image, namespace='default', labels=None, container_name=None, ports=None,
                               template_labels=None, replicas=1):
        """
        构造一个deployment的yaml文件进行部署
        :param name: deployment的名称
        :param image: 需要拉取的镜像名称
        :param namespace: 部署的命名空间
        :param labels: deployment的标签
        :param container_name: 容器的名字
        :param ports: 容器的端口
        :param template_labels: replicas的选择标签
        :param replicas: 要部署的容器的数量
        :return:
        """
        deployment = client.ExtensionsV1beta1Deployment()
        """
        填充deployment的元数据
        """
        deployment.api_version = "extensions/v1beta1"
        deployment.kind = "Deployment"
        deployment.metadata = client.V1ObjectMeta(name=name, labels=labels,namespace=namespace)
        port = []
        for p in ports:
            port.append(client.V1ContainerPort(name=p.name, container_port=p.port, protocol=p.protocol))
        """
        构造容器(container)模版
        """
        container = client.V1Container(name=container_name, image=image, ports=port)
        """
        构造replicas的模版
        """
        template = client.V1PodTemplateSpec(metadata=client.V1ObjectMeta(labels=template_labels),
                                            spec=client.V1PodSpec(container=[container]))
        """
        构造deployment的规范
        """
        spec = client.ExtensionsV1beta1DeploymentSpec(replicas=replicas, template=template, )
        deployment.spec = spec

        return deployment


if __name__ == '__main__':
    ext = Deployments()
    ext.get_deployment_detail(name='nginx')