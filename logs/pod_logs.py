#!/usr/local/miniconda2/bin/python
# _*_ coding:utf-8 _*_
"""
# @Project : docker-dashboard
# @Time    : 2018/10/17 下午11:10
# @Author  : zhangchengcheng
# @FileName: pod_logs.py
# @Github  : https://github.com/sweetcczhang
"""

from logs import kube_logs


class PodLogs(kube_logs.KubeLogs):

    # cpu cpu/limit cpu/usage_rate cpu/request
    # memory memory/usage memory/working_set memory/request memory/limit
    # network network/rx_rate network/tx_rate
    # filesystem filesystem/usage filesystem/limit
    def pod_data(self, namespace, pod_name):
        """
        获取pod的监控数据其中包括pod：
        cpu的使用情况
        memory的使用情况
        network的使用情况
        filesystem的使用情况
        :param namespace:
        :param pod_name:
        :return:
        """
        res = {}
        print(namespace)
        print(pod_name)
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
        """
        cpu的使用量
        """
        (used, time) = self.podquery("cpu/usage_rate", namespace, pod_name)
        res["cpu"]["usage_rate"].setdefault("sum", used)
        res["cpu"]["usage_rate"].setdefault("time", time)
        """
        cpu的使用限制
        """
        (used, time) = self.podquery("cpu/limit", namespace, pod_name)
        res["cpu"]["limit"].setdefault("sum", used)
        res["cpu"]["limit"].setdefault("time", time)
        """
        cpu的请求量
        """
        (used, time) = self.podquery("cpu/request", namespace, pod_name)
        res["cpu"]["request"].setdefault("sum", used)
        res["cpu"]["request"].setdefault("time", time)

        """
        memory的使用情况
        """
        (used, time) = self.podquery("memory/usage", namespace, pod_name)
        res["memory"]["usage"].setdefault("sum", used)
        res["memory"]["usage"].setdefault("time", time)

        (used, time) = self.podquery("memory/limit", namespace, pod_name)
        res["memory"]["limit"].setdefault("sum", used)
        res["memory"]["limit"].setdefault("time", time)

        (used, time) = self.podquery("memory/request", namespace, pod_name)
        res["memory"]["request"].setdefault("sum", used)
        res["memory"]["request"].setdefault("time", time)

        (used, time) = self.podquery("memory/working_set", namespace, pod_name)
        res["memory"]["working_set"].setdefault("sum", used)
        res["memory"]["working_set"].setdefault("time", time)

        """
        网络的使用情况
        """
        (used, time) = self.podquery("network/tx_rate", namespace, pod_name)
        res["network"]["tx_rate"].setdefault("sum", used)
        res["network"]["tx_rate"].setdefault("time", time)

        (used, time) = self.podquery("network/rx_rate", namespace, pod_name)
        res["network"]["rx_rate"].setdefault("sum", used)
        res["network"]["rx_rate"].setdefault("time", time)

        """
        文件系统的使用情况
        """
        (used, time) = self.podquery("filesystem/usage", namespace, pod_name)
        res["filesystem"]["usage"].setdefault("sum", used)
        res["filesystem"]["usage"].setdefault("time", time)

        (used, time) = self.podquery("filesystem/limit", namespace, pod_name)
        res["filesystem"]["limit"].setdefault("sum", used)
        res["filesystem"]["limit"].setdefault("time", time)

        return res