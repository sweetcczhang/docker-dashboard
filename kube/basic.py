#!/usr/local/miniconda2/bin/python
# _*_ coding:utf-8 _*_
"""
# @Project : docker-dashboard
# @Time    : 2018/10/12 上午10:04
# @Author  : zhangchengcheng
# @FileName: basic.py
# @Github  : https://github.com/sweetcczhang
"""
from kube.rest import configKube as conf
from datetime import datetime
import pytz


class Client(object):

    def __init__(self):
        self.v1_client = conf.get_core_v1_api()
        self.ext_client = conf.get_extensions()

    def v1_client(self):
        return self.v1_client

    def ext_client(self):
        return self.ext_client

    def pod_detail(self, pod):
        name = pod.metadata.name
        labels = pod.metadata.labels
        label = ''
        for key, value in labels.items():
            label = label + key + '=' + value + ','
        label = label.encode('utf-8')
        label = label[:len(label) - 1]
        namespace = pod.metadata.namespace
        image = pod.spec.containers[0].name
        node_name = pod.spec.node_name
        status = pod.status.phase
        create_time = pod.metadata.creation_timestamp
        now_time = datetime.utcnow().replace(tzinfo=pytz.timezone("UTC"))
        days = (now_time - create_time).days
        create_time = str(create_time)
        create_time = create_time[:len(create_time) - 6]
        temp = {'name': name, 'label': label, 'namespace': namespace, 'image': image, 'nodeName': node_name,
                'status': status, 'createTime': create_time, 'days': days}
        return temp

    def pod_list(self, api_response):
        lists = []
        for api in api_response:
            temp = self.pod_detail(pod=api)
            lists.append(temp)
        return lists

    def replicas_set_detail(self, replicas_set):
        name = replicas_set.metadata.name
        space = replicas_set.metadata.namespace
        create_time = replicas_set.metadata.creation_timestamp
        now_time = datetime.utcnow().replace(tzinfo=pytz.timezone("UTC"))
        days = (now_time - create_time).days
        create_time = str(create_time)
        create_time = create_time[:len(create_time) - 6]
        labels = replicas_set.metadata.labels
        label = ''
        for key, value in labels.items():
            label = label + key.encode('utf-8') + ":" + value + ","
        label = label[:len(label) - 1]
        replicas = replicas_set.spec.replicas
        selectors = replicas_set.spec.selector.match_labels
        selector = ''
        for key, value in selectors.items():
            selector = selector + key.encode('utf-8') + ':' + value + ','
        selector = selector[:len(selector) - 1]
        image = replicas_set.spec.template.spec.containers[0].image
        available_replicas = replicas_set.status.available_replicas
        temp = {'name': name, 'namespace': space, 'days': days, 'createTime': create_time,
                'label': label, 'replicas': replicas, 'selector': selector, 'image': image,
                'availableReplicas': available_replicas}

        return temp

    def replicas_set_list(self, api_response):
        lists = []
        for api in api_response:
            temp = self.replicas_set_detail(api)
            lists.append(temp)
        return lists
