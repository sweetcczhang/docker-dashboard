#!/usr/local/miniconda2/bin/python
# _*_ coding:utf-8 _*_
"""
# @Project : docker-dashboard
# @Time    : 2018/10/15 下午12:05
# @Author  : zhangchengcheng
# @FileName: kube_hostInfo.py
# @Github  : https://github.com/sweetcczhang
"""


from kube import basic
from kubernetes.client.rest import ApiException
from kubernetes import client
import os


class HostInfo(basic.Client):

    def get_host_info(self):
        node_list = []
        try:
            host = self.v1_client.list_node()
            for i in host.items:
                s = str(i.metadata.creation_timestamp)
                create_time = s[:len(s) - 6]
                name = i.metadata.name
                host_ip = i.spec.external_id
                status = 'NotReady'
                os = i.status.node_info.os_image
                docker_version = i.status.node_info.container_runtime_version
                cpu = i.status.capacity[u'cpu']
                memory = i.status.capacity[u'memory']
                memory = memory[:len(memory) - 2]
                memory = int(memory) / 1024
                memory = str(memory) + 'Mi'
                status_1 = i.status.conditions[-1].status
                if status_1 == 'True':
                    status = 'Ready'
                temp = {'name': name, 'hostIp': host_ip, 'status': status, 'os': os, 'dockerVersion': docker_version,
                        'cpu': cpu, 'memory': memory, 'createTime': create_time}
                node_list.append(temp)
                print temp
        except ApiException as e:
            print e
        print node_list
        return node_list


if __name__ == '__main__':
    v1 = HostInfo()
    v1.get_host_info()