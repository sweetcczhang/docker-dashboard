#!/usr/local/miniconda2/bin/python
# _*_ coding:utf-8 _*_
"""
# @Project : docker-dashboard
# @Time    : 2018/10/12 上午10:14
# @Author  : zhangchengcheng
# @FileName: kube_service.py
# @Github  : https://github.com/sweetcczhang
"""

from kube import basic
from kubernetes.client.rest import ApiException
from kubernetes import client
import os


class Services(basic.Client):

    def get_service_info(self, namespace=None):
        """
        获取指定命名空间的所有service，当namespace为空的时候，获取所有命名空间的数据
        :param namespace:
        :return:
        """
        lists = []
        try:
            if namespace is None:
                services_list = self.v1_client.list_service_for_all_namespaces().items
            else:
                services_list = self.v1_client.list_namespaced_service(namespace=namespace,).items
            for i in services_list:
                name = i.metadata.name
                namespace = i.metadata.namespace
                label = i.metadata.labels
                labels = ''
                if label is not None:
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
                temp = {"name": name, "namespace": namespace, "labels": labels,
                        "cluster_ip": cluster_ip, "type": hello, "port": port}
                print temp
                lists.append(temp)
        except ApiException as e:
            print e

        return len(lists), lists

    def create_service(self, name, labels, namespace='default', port_type=None, s_port=None, selector=None):
        """
        一个service主要分为三部分：
        元数据:metadata
        规范:spec
        状态:status
        :param name:
        :param labels:
        :param s_port:
        :param namespace:
        :param port_type:
        :param selector:
        :return:
        """

        service = client.V1Service()

        """
        构造metadata部分的数据
        """
        metadata = client.V1ObjectMeta()
        metadata.name = name
        metadata.labels = labels

        """
        构造spec部分的数据
        """
        s_spec = client.V1ServiceSpec()
        s_spec.type = port_type
        s_spec.selector = selector
        ports = []
        for p in s_port:
            v_port = client.V1ServicePort(name=p.name, node_port=p.nodePort, port=p.port, target_port=p.targetPort,
                                          protocol=p.protocol)
            ports.append(v_port)

        s_spec.ports = ports
        service.metadata = metadata
        service.spec = s_spec

        self.v1_client.create_namespaced_service(namespace=namespace, body=service)

    def get_service_detail(self, name, namespace='default'):
        """
        获取指定的名称的service的名称
        :param name:
        :param namespace:
        :return:
        """
        service_detail = {}
        try:
            api_response = self.v1_client.read_namespaced_service(name=name, namespace=namespace)
            name = api_response.metadata.name
            namespace = api_response.metadata.namespace
            label = api_response.metadata.labels
            labels = ''
            for key, value in label.items():
                labels = labels + key + '=' + value + ','
            labels = labels.encode('utf-8')
            cluster_ip = api_response.spec.cluster_ip
            hello = api_response.spec.type
            ports = api_response.spec.ports[0]
            port = ''
            s = ports.node_port
            if s != 'None':
                port = str(ports.node_port) + ':'
            port = port + str(ports.port) + "/TCP"
            create_time = api_response.metadata.creation_timestamp
            create_time = str(create_time)
            create_time = create_time[:len(create_time)-6]
            service_detail = {"name": name, "namespace": namespace, "labels": labels, "clusterIp": cluster_ip,
                              "type": hello, "port": port, "createTime": create_time}
            print create_time
            print service_detail
        except ApiException as e:
            print e
        return service_detail

    def get_service_from_label_selector(self, label_selector, namespace):
        service_list = {}
        try:
            api_response = self.v1_client.list_namespaced_service(namespace=namespace, label_selector=label_selector)
            service_list = self.service_list(api_response)

        except ApiException as e:
            print e
        return len(service_list), service_list


if __name__ == '__main__':
    v1 = Services()
    v1.get_service_info()
    # v1.get_service_detail(name='example-service')
    # basepath = os.path.dirname(__file__)
    # print basepath