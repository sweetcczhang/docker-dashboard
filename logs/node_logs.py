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
import threading
LOCK = threading.RLock()


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
        # print (ip)
        """
        the cpu of node
        """
        res["cpu"] = {}
        res["cpu"]["usage_rate"] = {}
        # res["cpu"]["limit"] = {}
        res["cpu"]["request"] = {}

        """
        the memory of node
        """
        res["memory"] = {}
        res["memory"]["usage"] = {}
        res["memory"]["working_set"] = {}
        res["memory"]["request"] = {}
        # res["memory"]["limit"] = {}

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
        LOCK.acquire()
        (used, time) = self.node_query("cpu/usage_rate", ip)
        # print used
        used = used[1:]
        use = []
        for c in used:
            if c is None:
                c = use[-1]
            c = c/(1000.0 * 2.0)
            use.append(c)
        i = len(use)
        # print i
        a = use[i - 2]
        use[i - 1] = a
        # use[len(use) - 1] = use[len(use) - 2]
        # ßßprint use
        res["cpu"]["usage_rate"].setdefault("sum", use)
        res["cpu"]["usage_rate"].setdefault("time", time[1:])

        # (used, time) = self.node_query("cpu/limit", ip)
        # res["cpu"]["limit"].setdefault("sum", used)
        # res["cpu"]["limit"].setdefault("time", time)

        (used, time) = self.node_query("cpu/request", ip)
        used = used[1:]
        use = []
        for c in used:
            if c is None:
                c = use[-1]
            c/(1000.0 * 2.0)
            use.append(c)

        res["cpu"]["request"].setdefault("sum", use)
        res["cpu"]["request"].setdefault("time", time[1:])

        """
        memory的使用情况
        """
        (used, time) = self.node_query("memory/usage", ip)
        used = used[1:]
        use = []
        for c in used:
            if c is None:
                c = use[-1]
            c = c / (1024.0 * 1024.0 * 2.0)
            use.append(c)
        res["memory"]["usage"].setdefault("sum", use)
        res["memory"]["usage"].setdefault("time", time[1:])

        # (used, time) = self.node_query("memory/limit", ip)
        # res["memory"]["limit"].setdefault("sum", used)
        # res["memory"]["limit"].setdefault("time", time)

        (used, time) = self.node_query("memory/request", ip)
        used = used[1:]
        use = []
        for c in used:
            if c is None:
                c = use[-1]
            c = c / (1024.0 * 1024.0 * 2.0)
            use.append(c)
        res["memory"]["request"].setdefault("sum", use)
        res["memory"]["request"].setdefault("time", time[1:])

        (used, time) = self.node_query("memory/working_set", ip)
        used = used[1:]
        use = []
        for c in used:
            if c is None:
                c = use[-1]
            c = c / (1024.0 * 1024.0 * 2.0)
            use.append(c)
        res["memory"]["working_set"].setdefault("sum", use)
        res["memory"]["working_set"].setdefault("time", time)

        """
        network的使用情况
        """
        (used, time) = self.node_query("network/tx_rate", ip)

        res["network"]["tx_rate"].setdefault("sum", used[1:])
        res["network"]["tx_rate"].setdefault("time", time[1:])

        (used, time) = self.node_query("network/rx_rate", ip)
        res["network"]["rx_rate"].setdefault("sum", used[1:])
        res["network"]["rx_rate"].setdefault("time", time[1:])

        """
        filesystem的使用情况
        """
        (used, time) = self.node_query("filesystem/usage", ip)
        used = used[1:]
        use = []
        for c in used:
            if c is None:
                c = use[-1]
            c = c / (1024.0 * 1024.0 * 2.0)
            use.append(c)
        res["filesystem"]["usage"].setdefault("sum", use)
        res["filesystem"]["usage"].setdefault("time", time[1:])
        used = used[1:]
        use = []
        for c in used:
            if c is None:
                c = use[-1]
            c = c / (1024.0 * 1024.0 * 2.0)
            use.append(c)
        (used, time) = self.node_query("filesystem/limit", ip)
        res["filesystem"]["limit"].setdefault("sum", use)
        res["filesystem"]["limit"].setdefault("time", time[1:])
        LOCK.release()
        return res


if __name__ == '__main__':
    test =[10, 10, 10]
    b =[]
    for i in test:
        b.append(i/2)
    print b