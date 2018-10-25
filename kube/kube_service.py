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

    def get_service_info(self, page=1, limit=10, namespace=None):
        """
        获取指定命名空间的所有service，当namespace为空的时候，获取所有命名空间的数据
        :param page:
        :param limit:
        :param namespace:
        :return:
        """
        lists = []
        try:
            if namespace is None:
                services_list = self.v1_client.list_service_for_all_namespaces(_continue=page, limit=limit).items
            else:
                services_list = self.v1_client.list_namespaced_service(namespace=namespace, _continue=page, limit=limit)
            for i in services_list:
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
                temp = {"name": name, "namespace": namespace, "labels": labels,
                        "cluster_ip": cluster_ip, "type": hello, "port": port}
                print temp
                lists.append(temp)
        except ApiException as e:
            print e

        return lists

    def create_service(self, name, labels, port=80, namespace='default', node_port=None, protocol='TCP', port_type=None,
                       selector=None):
        """
        一个service主要分为三部分：
        元数据:metadata
        规范:spec
        状态:status
        :param name:
        :param labels:
        :param port:
        :param namespace:
        :param node_port:
        :param protocol:
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
        ports = [client.V1ServicePort(name=None, node_port=node_port, port=port, protocol=protocol)]

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

    def get_service_from_label_selector(self, label_selector):
        service_detail = {}
        try:
            api_response = self.v1_client.list_service_for_all_namespaces(label_selector=label_selector)
            service_detail = self.service_detail(api_response)

        except ApiException as e:
            print e
        return service_detail


if __name__ == '__main__':
    # v1 =Service()
    # v1.get_service_detail(name='example-service')
    basepath = os.path.dirname(__file__)
    print basepath