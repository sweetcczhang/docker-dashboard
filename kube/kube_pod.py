#!/usr/local/miniconda2/bin/python
# _*_ coding:utf-8 _*_
"""
# @Project : docker-dashboard
# @Time    : 2018/10/12 下午5:12
# @Author  : zhangchengcheng
# @FileName: kube_pod.py
# @Github  : https://github.com/sweetcczhang
"""
from kube import basic
from kubernetes.client.rest import ApiException
from datetime import datetime
from kubernetes import watch, client
import pytz


class Pods(basic.Client):

    def get_pod_details(self, name, namespace='default'):
        """
        列出某个pod的详细信息
        :param name:
        :param namespace:
        :return:
        """
        pod_detail = {}
        try:
            api = self.v1_client.read_namespaced_pod(name=name, namespace=namespace)

            pod_detail = self.pod_detail(pod=api)

        except ApiException as e:
            print e
        return pod_detail

    def get_all_pods(self, page=1, limit=1, namespace=None):
        """
        列出指定的命名空间中的所有pod或者是所有命名空间中的pod
        :param page:
        :param limit:
        :param namespace:
        :return:
        """
        lists = []
        try:
            if namespace is None:
                api_response = self.v1_client.list_pod_for_all_namespaces(_continue=page, limit=limit).items
            else:
                api_response = self.v1_client.list_namespaced_pod(_continue=page, limit=limit,
                                                                  namespace=namespace).items
            lists = self.pod_list(api_response=api_response)
            print api_response

        except ApiException as e:
            print e

        return lists

    def get_watch(self, name, namespace='default'):
        w = watch.Watch()
        log = w.stream(self.v1_client.read_namespaced_pod_log, name=name, namespace=namespace)
        for l in log:
            print l
        # print w.stream(self.v1_client.list_pod_for_all_namespaces)
        # for event in w.stream(self.v1_client.list_pod_for_all_namespaces):
        #     print event
        #     print ("Event: %s %s %s" % (event['type'], event['object'].kind, event['object'].metadata.name))

    def create_pod(self, name, image, labels=None, namespace='default', ports=None, commands=None, args=None,
                   hostname=None, limits=None, requests=None):
        """
        构造pod对象并调用相应的接口进行创建一个pod对象主要分为三部分：
        1.元数据信息：metadata
        2.规范：spec
        3.状态：status
        :param name:
        :param image:
        :param labels:
        :param namespace:
        :param ports:
        :param commands:
        :param args:
        :param hostname:
        :param limits:
        :param requests:
        :return:
        """
        """
        构造一个pod对象
        """
        pod = client.V1Pod()

        """
        构建metdata部分
        """
        metadata = client.V1ObjectMeta(name=name, labels=labels)

        """
        构造spec部分
        """
        spec = client.V1PodSpec(hostname=hostname)
        containers = client.V1Container(image=image, args=args, commands=commands, ports=ports)
        resources = client.V1ResourceRequirements(limits=limits, requests=requests)
        containers.resources = resources
        spec.containers = containers

        """
        对pod各个部分的数据进行填充
        """
        pod.metadata = metadata
        pod.spec = spec

        """
        调用接口创建pod对象
        """
        self.v1_client.create_namespaced_pod(namespace=namespace, body=pod)

    def get_pod_log(self, name, namespace='default'):
        """
        获取指定pod的日志以str的形式返回
        :param name:
        :param namespace:
        :return:
        """
        log = ''
        try:
            log = self.v1_client.read_namespaced_pod_log(name=name, namespace=namespace)
            print log
        except ApiException as e:
            print e

        return log

    def get_pod_from_label_or_field(self, label_selector=None, field_selector=None,
                                    namespace='default'):
        """
        通过label_selector或者field_selector来获取符合
        条件的pod。
        :param label_selector:
        :param field_selector:
        :param namespace:
        :return:
        """
        field_selector = 'spec.nodeName=' + field_selector
        lists = []
        length = 0
        try:
            if label_selector is None:
                api_response = self.v1_client.list_pod_for_all_namespaces(field_selector=field_selector).items
            else:
                api_response = self.v1_client.list_namespaced_pod(namespace=namespace,
                                                                  label_selector=label_selector).items

            length = len(api_response)
            lists = self.pod_list(api_response=api_response)
            print api_response
        except ApiException as e:
            print e

        return length, lists


if __name__ == '__main__':
    v1 = Pods()
    print "zcc"
    v1.get_pod_from_node(field_selector='10.108.211.22')
    # v1.get_all_pods()
    # v1.get_pod_log(name='nginx-774d74897-v7v2f')
    # v1.get_watch(name='nginx-774d74897-v7v2f')
    # v1.get_watch()