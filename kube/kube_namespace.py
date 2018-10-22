#!/usr/local/miniconda2/bin/python
# _*_ coding:utf-8 _*_
"""
# @Project : docker-dashboard
# @Time    : 2018/10/14 下午5:47
# @Author  : zhangchengcheng
# @FileName: kube_namespace.py
# @Github  : https://github.com/sweetcczhang
"""
from kube import basic
from kubernetes.client.rest import ApiException
from datetime import datetime
import pytz
from kubernetes import client


class Namespace(basic.Client):

    def list_all_namespace(self):
        """
        获取所有的命名空间
        :return:
        """
        lists = []
        try:
            api_response = self.v1_client.list_namespace().items
            for api in api_response:
                name = api.metadata.name
                create_time = api.metadata.creation_timestamp
                now_time = datetime.utcnow().replace(tzinfo=pytz.timezone("UTC"))
                days = (now_time-create_time).days
                create_time = str(create_time)
                create_time = create_time[:len(create_time) - 6]
                status = api.status.phase
                temp = {'name': name, 'days': days, 'createTime': create_time, 'status': status}
                lists.append(temp)
            print api_response
        except ApiException as e:
            print e

        return lists

    def create_namespace(self, name):
        sp = client.V1Namespace(metadata=client.V1ObjectMeta(name=name))
        try:
            api_response = self.v1_client.create_namespace(body=sp)
            print api_response
        except ApiException as e:
            print e


if __name__ == '__main__':
    v1 = Namespace()
    v1.list_all_namespace()