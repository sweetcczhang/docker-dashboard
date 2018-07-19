#!/usr/local/miniconda2/bin/python
# _*_ coding:utf-8 _*_
"""
# @Time   : 2018/7/18 22:55
# @Author : 张城城
"""
import threading


class HostStreamThread(threading.Thread):

    def __init__(self, ws, resp):
        super(HostStreamThread, self).__init__()
        self.ws = ws
        self.resp = resp

    def run(self):
        # return resp
        while not self.ws.closed:
            try:
                result = self.resp.recv(2048)
                self.ws.send(result)
            except Exception as e:
                print("host daemon socket err: %s" % e)
                self.ws.close()
                self.resp.close()
                break