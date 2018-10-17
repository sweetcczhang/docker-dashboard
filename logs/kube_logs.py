#!/usr/local/miniconda2/bin/python
# _*_ coding:utf-8 _*_
"""
# @Project : docker-dashboard
# @Time    : 2018/10/17 下午8:57
# @Author  : zhangchengcheng
# @FileName: kube_logs.py
# @Github  : https://github.com/sweetcczhang
"""

from influxdb import InfluxDBClient
from datetime import datetime, timedelta


class KubeLogs(object):

    def __init__(self, ip='10.108.210.194', ports='32169', user_name='root', pwd='root', db='k8s'):
        self.client = InfluxDBClient(ip, ports, user_name, pwd, db)

    def node_query(self, table_name, ip):
        """
        使用influxdb保存监控的时序数据。
        通过数据库名称和节点ip来查询指定主机的数据
        :param table_name:
        :param ip:
        :return:
        """
        used = []
        time = []

        sql = "SELECT sum(value) FROM k8s.\"default\".\"{table_name}\" WHERE type = 'node' AND" \
              " nodename =~ /{ip}$/ AND time > now() - 30m GROUP BY time(1m)".format(table_name=table_name, ip=ip)
        set = self.client.query(sql)
        self.client.close()
        for v1 in set:
            for v2 in v1:
                date = datetime.strptime(v2['time'], "%Y-%m-%dT%H:%M:%SZ")
                local = date + timedelta(hours=8)
                time.append(datetime.strftime(local, '%Y-%m-%d %H:%M:%S'))
                used.append(v2['sum'])
        return used, time

    def pod_query(self, table_name, namespace, pod_name):
        """

        :param table_name:
        :param namespace:
        :param pod_name:
        :return:
        """
        used = []
        time = []
        if table_name[0] == "c" or table_name[0] == "f":
            types = "pod_container"
        else:
            types = "pod"
        sql = "SELECT sum(value) FROM k8s.\"default\".\"{table_name}\" WHERE  type = '{type}'" \
              " AND namespace_name =~ /{namespace}$/ AND pod_name =~ /{pod_name}$/ AND time > now() - 30m" \
              " GROUP BY time(1m)".format(table_name=table_name, type=types, pod_name=pod_name, namespace=namespace)
        pod_list = self.client.query(sql)
        self.client.close()
        for v1 in pod_list:
            for v2 in v1:
                date = datetime.strptime(v2['time'], "%Y-%m-%dT%H:%M:%SZ")
                local = date + timedelta(hours=8)
                time.append(datetime.strftime(local, '%Y-%m-%d %H:%M:%S'))
                used.append(v2['sum'])
        return used, time

