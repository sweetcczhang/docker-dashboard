#!/usr/local/miniconda2/bin/python
# _*_ coding:utf-8 _*_
"""
# @Project : docker-dashboard
# @Time    : 2018/10/15 上午11:36
# @Author  : zhangchengcheng
# @FileName: kube_replicas_set.py
# @Github  : https://github.com/sweetcczhang
"""
from kube import basic
from kubernetes.client.rest import ApiException


class ReplicasSet(basic.Client):

    def get_all_replicas_set(self, namespace=None):
        """
        获取指定命名空间中的所有的replicas set，若namespace为None则查询所有的命名空间
        中的replicas set
        :param namespace:
        :return:
        """
        lists = []
        try:
            if namespace is None:
                api_response = self.ext_client.list_replica_set_for_all_namespaces().items
            else:
                api_response = self.ext_client.list_namespaced_replica_set(namespace=namespace).items

            lists = self.replicas_set_list(api_response=api_response)

            print api_response
        except ApiException as e:
            print e
        return lists

    def delete_replicas_set(self, name, namespace='default'):
        """
        删除指定命名空间中指定名称的replicas set
        :param name:
        :param namespace:
        :return:
        """
        try:
            self.ext_client.delete_namespaced_replica_set(name=name, namespace=namespace)
        except ApiException as e:
            print e

    def get_replicas_set_from_labels(self, label_selector, namespace='default'):
        """
        通过label selector来查询 replicas set 供 deployment使用
        :param label_selector:
        :param namespace:
        :return:
        """
        lists = {}
        try:
            api_response = self.ext_client.list_namespaced_replica_set(namespace=namespace,
                                                                       label_selector=label_selector).items
            lists = self.replicas_set_detail(api_response)
        except ApiException as e:
            print e
        return lists


if __name__ == '__main__':
    ext = ReplicasSet()
    # ext.get_pod_from_labels()
    ext.get_all_replicas_set()
