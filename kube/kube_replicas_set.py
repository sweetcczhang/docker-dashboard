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
from kubernetes import client
from datetime import datetime
import pytz


class ReplicasSet(basic.Client):

    def get_all_replicas_set(self, namespace=None):

        lists = []
        try:
            if namespace is None:
                api_response = self.ext_client.list_replica_set_for_all_namespaces().items
            else:
                api_response = self.ext_client.list_namespaced_replica_set(namespace=namespace).items

            for api in api_response:
                name = api.metadata.name
                space = api.metadata.namespace
                create_time = api.metadata.creation_timestamp
                now_time = datetime.utcnow().replace(tzinfo=pytz.timezone("UTC"))
                days = (now_time - create_time).days
                create_time = str(create_time)
                create_time = create_time[:len(create_time) - 6]
                labels = api.metadata.labels
                for key, value in labels.items():
                    label = label + key + '=' + value + ','
                label = label.encode('utf-8')
                label = label[:len(label)-1]

            print api_response
        except ApiException as e:
            print e

    def get_pod_from_labels(self):
        api_response = self.v1_client.list_namespaced_pod(namespace='default', label_selector='nginx-774d74897')
        print api_response


if __name__ == '__main__':
    ext = ReplicasSet()
    #ext.get_pod_from_labels()
    ext.get_all_replicas_set()
