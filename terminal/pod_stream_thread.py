#!/usr/local/miniconda2/bin/python
# _*_ coding:utf-8 _*_
"""
# @Project : docker-dashboard
# @Time    : 2018/10/25 下午3:40
# @Author  : zhangchengcheng
# @FileName: pod_stream_thread.py
# @Github  : https://github.com/sweetcczhang
"""
import threading


class StreamThread(threading.Thread):

    def __init__(self, ws, resp):
        super(StreamThread, self).__init__()
        self.ws = ws
        self.resp = resp

    def run(self):
        # return resp
        while (not self.ws.closed) and (self.resp.is_open()):
            try:
                self.resp.update(timeout=1)
                if self.resp.peek_stdout():
                    message = self.resp.read_stdout()
                    self.ws.send(str(message))
                    print("STDOUT: %s" % message)
                if self.resp.peek_stderr():
                    message = self.resp.read_stderr()
                    self.ws.send(str(message))
                    print("STDERR: %s" % message)
            except Exception as e:
                print("docker daemon socket err: %s" % e)
                self.ws.close()
                self.resp.close()
                break
