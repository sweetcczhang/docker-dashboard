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

    def node_query(self, tabname, ip):
        sum = []
        time = []

        sql = "SELECT sum(value) FROM k8s.\"default\".\"{tabname}\" WHERE type = 'node' AND" \
              " nodename =~ /{ip}$/ AND time > now() - 30m GROUP BY time(1m)".format(tabname=tabname, ip=ip)
        set = self.client.query(sql)
        self.client.close()
        for v1 in set:
            for v2 in v1:
                date = datetime.strptime(v2['time'], "%Y-%m-%dT%H:%M:%SZ")
                local = date + timedelta(hours=8)
                time.append(datetime.strftime(local, '%Y-%m-%d %H:%M:%S'))
                sum.append(v2['sum'])
        return sum, time

    def pod_query(self, table_name, namespace, pod_name):
        used = []
        time = []
        if table_name[0] == "c" or table_name[0] == "f":
            types = "pod_container"
        else:
            types = "pod"
        sql = "SELECT sum(value) FROM k8s.\"default\".\"{tabname}\" WHERE  type = '{type}'" \
              " AND namespace_name =~ /{namespace}$/ AND pod_name =~ /{podname}$/ AND time > now() - 30m" \
              " GROUP BY time(1m)".format(tabname=table_name, type=types, podname=pod_name, namespace=namespace)
        pod_list = self.client.query(sql)
        self.client.close()
        for v1 in pod_list:
            for v2 in v1:
                date = datetime.strptime(v2['time'], "%Y-%m-%dT%H:%M:%SZ")
                local = date + timedelta(hours=8)
                time.append(datetime.strftime(local, '%Y-%m-%d %H:%M:%S'))
                used.append(v2['sum'])
        return used, time

    def node_data(self, ip):
        # cpu cpu/limit cpu/usage_rate cpu/request
        # memory memory/usage memory/working_set memory/request memory/limit
        # network network/rx_rate network/tx_rate
        # filesystem filesystem/usage filesystem/limit
        """

        :param ip:
        :return:
        """
        res = {}
        res["cpu"] = {}
        res["cpu"]["usage_rate"] = {}
        res["cpu"]["limit"] = {}
        res["cpu"]["request"] = {}

        res["memory"] = {}
        res["memory"]["usage"] = {}
        res["memory"]["working_set"] = {}
        res["memory"]["request"] = {}
        res["memory"]["limit"] = {}

        res["network"] = {}
        res["network"]["rx_rate"] = {}
        res["network"]["tx_rate"] = {}

        res["filesystem"] = {}
        res["filesystem"]["usage"] = {}
        res["filesystem"]["limit"] = {}

        (used, time) = self.nodequery("cpu/usage_rate",ip)
        res["cpu"]["usage_rate"].setdefault("sum", used)
        res["cpu"]["usage_rate"].setdefault("time", time)

        (used, time) = self.nodequery("cpu/limit", ip)
        res["cpu"]["limit"].setdefault("sum", used)
        res["cpu"]["limit"].setdefault("time", time)

        (used, time) = self.nodequery("cpu/request", ip)
        res["cpu"]["request"].setdefault("sum", used)
        res["cpu"]["request"].setdefault("time", time)

        (used, time) = self.nodequery("memory/usage", ip)
        res["memory"]["usage"].setdefault("sum", used)
        res["memory"]["usage"].setdefault("time", time)

        (used, time) = self.nodequery("memory/limit", ip)
        res["memory"]["limit"].setdefault("sum", used)
        res["memory"]["limit"].setdefault("time", time)

        (used, time) = self.nodequery("memory/request", ip)
        res["memory"]["request"].setdefault("sum", used)
        res["memory"]["request"].setdefault("time", time)

        (used, time) = self.nodequery("memory/working_set", ip)
        res["memory"]["working_set"].setdefault("sum", used)
        res["memory"]["working_set"].setdefault("time", time)

        (used, time) = self.nodequery("network/tx_rate", ip)
        res["network"]["tx_rate"].setdefault("sum", used)
        res["network"]["tx_rate"].setdefault("time", time)

        (used, time) = self.nodequery("network/rx_rate", ip)
        res["network"]["rx_rate"].setdefault("sum", used)
        res["network"]["rx_rate"].setdefault("time", time)

        (used, time) = self.nodequery("filesystem/usage", ip)
        res["filesystem"]["usage"].setdefault("sum", used)
        res["filesystem"]["usage"].setdefault("time", time)

        (used, time) = self.nodequery("filesystem/limit", ip)
        res["filesystem"]["limit"].setdefault("sum", used)
        res["filesystem"]["limit"].setdefault("time", time)

        return res

    def pod_data(self, namespace, podname):
        # cpu cpu/limit cpu/usage_rate cpu/request
        # memory memory/usage memory/working_set memory/request memory/limit
        # network network/rx_rate network/tx_rate
        # filesystem filesystem/usage filesystem/limit
        """

        :return:
        """
        res = {}
        print(namespace)
        print(podname)
        res["cpu"] = {}
        res["cpu"]["usage_rate"] = {}
        res["cpu"]["limit"] = {}
        res["cpu"]["request"] = {}
        res["memory"] = {}
        res["memory"]["usage"] = {}
        res["memory"]["working_set"] = {}
        res["memory"]["request"] = {}
        res["memory"]["limit"] = {}
        res["network"] = {}
        res["network"]["rx_rate"] = {}
        res["network"]["tx_rate"] = {}
        res["filesystem"] = {}
        res["filesystem"]["usage"] = {}
        res["filesystem"]["limit"] = {}

        (used, time) = self.podquery("cpu/usage_rate", namespace, podname)
        res["cpu"]["usage_rate"].setdefault("sum", used)
        res["cpu"]["usage_rate"].setdefault("time", time)

        (used, time) = self.podquery("cpu/limit", namespace, podname)
        res["cpu"]["limit"].setdefault("sum", used)
        res["cpu"]["limit"].setdefault("time", time)

        (used, time) = self.podquery("cpu/request", namespace, podname)
        res["cpu"]["request"].setdefault("sum", used)
        res["cpu"]["request"].setdefault("time", time)

        (used, time) = self.podquery("memory/usage", namespace, podname)
        res["memory"]["usage"].setdefault("sum", used)
        res["memory"]["usage"].setdefault("time", time)

        (used, time) = self.podquery("memory/limit", namespace, podname)
        res["memory"]["limit"].setdefault("sum", used)
        res["memory"]["limit"].setdefault("time", time)

        (used, time) = self.podquery("memory/request", namespace, podname)
        res["memory"]["request"].setdefault("sum", used)
        res["memory"]["request"].setdefault("time", time)

        (used, time) = self.podquery("memory/working_set", namespace, podname)
        res["memory"]["working_set"].setdefault("sum", used)
        res["memory"]["working_set"].setdefault("time", time)

        (used, time) = self.podquery("network/tx_rate", namespace, podname)
        res["network"]["tx_rate"].setdefault("sum", used)
        res["network"]["tx_rate"].setdefault("time", time)

        (used, time) = self.podquery("network/rx_rate", namespace, podname)
        res["network"]["rx_rate"].setdefault("sum", used)
        res["network"]["rx_rate"].setdefault("time", time)

        (used, time) = self.podquery("filesystem/usage", namespace, podname)
        res["filesystem"]["usage"].setdefault("sum", used)
        res["filesystem"]["usage"].setdefault("time", time)

        (used, time) = self.podquery("filesystem/limit", namespace, podname)
        res["filesystem"]["limit"].setdefault("sum", used)
        res["filesystem"]["limit"].setdefault("time", time)

        return res
