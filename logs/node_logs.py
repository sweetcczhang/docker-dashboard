#!/usr/local/miniconda2/bin/python
# _*_ coding:utf-8 _*_
"""
# @Project : docker-dashboard
# @Time    : 2018/10/17 下午11:10
# @Author  : zhangchengcheng
# @FileName: node_logs.py
# @Github  : https://github.com/sweetcczhang
"""

from logs import kube_logs


class NodeLogs(kube_logs.KubeLogs):

    def node_data(self, ip):
        # cpu cpu/limit cpu/usage_rate cpu/request
        # memory memory/usage memory/working_set memory/request memory/limit
        # network network/rx_rate network/tx_rate
        # filesystem filesystem/usage filesystem/limit
        """
        查询获取指定主机数据的使用情况：其中主要包括4中数据cpu、network、memory、filesystem
        :param ip:特定的主机ip
        :return:
        """

        res = {}
        print (ip)
        """
        the cpu of node
        """
        res["cpu"] = {}
        res["cpu"]["usage_rate"] = {}
        res["cpu"]["limit"] = {}
        res["cpu"]["request"] = {}

        """
        the memory of node
        """
        res["memory"] = {}
        res["memory"]["usage"] = {}
        res["memory"]["working_set"] = {}
        res["memory"]["request"] = {}
        res["memory"]["limit"] = {}

        """
        the network of node
        """
        res["network"] = {}
        res["network"]["rx_rate"] = {}
        res["network"]["tx_rate"] = {}

        """
        the file use of node
        """
        res["filesystem"] = {}
        res["filesystem"]["usage"] = {}
        res["filesystem"]["limit"] = {}

        """
        cpu的使用情况
        """
        (used, time) = self.nodequery("cpu/usage_rate",ip)
        res["cpu"]["usage_rate"].setdefault("sum", used)
        res["cpu"]["usage_rate"].setdefault("time", time)

        (used, time) = self.nodequery("cpu/limit", ip)
        res["cpu"]["limit"].setdefault("sum", used)
        res["cpu"]["limit"].setdefault("time", time)

        (used, time) = self.nodequery("cpu/request", ip)
        res["cpu"]["request"].setdefault("sum", used)
        res["cpu"]["request"].setdefault("time", time)

        """
        memory的使用情况
        """
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

        """
        network的使用情况
        """
        (used, time) = self.nodequery("network/tx_rate", ip)
        res["network"]["tx_rate"].setdefault("sum", used)
        res["network"]["tx_rate"].setdefault("time", time)

        (used, time) = self.nodequery("network/rx_rate", ip)
        res["network"]["rx_rate"].setdefault("sum", used)
        res["network"]["rx_rate"].setdefault("time", time)

        """
        filesystem的使用情况
        """
        (used, time) = self.nodequery("filesystem/usage", ip)
        res["filesystem"]["usage"].setdefault("sum", used)
        res["filesystem"]["usage"].setdefault("time", time)

        (used, time) = self.nodequery("filesystem/limit", ip)
        res["filesystem"]["limit"].setdefault("sum", used)
        res["filesystem"]["limit"].setdefault("time", time)

        return res
