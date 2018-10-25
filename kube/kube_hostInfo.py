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
from datetime import datetime
import pytz


class HostInfo(basic.Client):

    def get_host_info(self):
        """
        获取指定集群中的所有主机
        :return:
        """
        node_list = []
        try:
            host = self.v1_client.list_node()
            print len(host.items)
            print host
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

        return len(node_list), node_list

    def host_detail(self, host_name):
        try:
            api_response = self.v1_client.read_node_status(name=host_name)
            cpu = api_response.status.capacity[u'cpu']
            memory = api_response.status.capacity[u'memory']
            memory = memory[:len(memory) - 2]
            memory = int(memory) / 1024
            memory = str(memory) + 'Mi'
            create_time = str(api_response.metadata.creation_timestamp)
            create_time = create_time[:len(create_time)-6]
            num_images = len(api_response.status.images)
            list_condition = self.get_condition(api_response.status.conditions)
            info = {'cpu': cpu, 'memory': memory, 'imagesNum': num_images, 'createTime': create_time}
            print list_condition
            print info
            return list_condition, info
        except ApiException as e:
            print e
            return None

    def get_condition(self, conditions):
        lists = []
        for i in conditions:
            now_time = datetime.utcnow().replace(tzinfo=pytz.timezone("UTC"))
            last_heartbeat_time = (now_time - i.last_heartbeat_time).seconds
            last_transition_time = (now_time-i.last_transition_time).days
            message = i.message
            reason = i.reason
            status = i.status
            types = i.type
            temp = {'type': types, 'status': status, 'last_heartbeat_time': last_heartbeat_time,
                    'lastTransitionTime': last_transition_time, 'message': message, 'reason': reason}
            lists.append(temp)
        return lists


if __name__ == '__main__':
    v1 = HostInfo()
    v1.host_detail(host_name='10.108.210.194')
    #v1.get_host_info()
