#!/usr/local/miniconda2/bin/python
# _*_ coding:utf-8 _*_
"""
# @Project : docker-dashboard
# @Time    : 2018/10/25 下午3:45
# @Author  : zhangchengcheng
# @FileName: host_client.py
# @Github  : https://github.com/sweetcczhang
"""
import paramiko
from paramiko.ssh_exception import AuthenticationException, SSHException


class HostClient(object):

    # def __init__(self, hostname, port, username, password):
    #     self.hostname = hostname
    #     self.port = port
    #     self.username = username
    #     self.password = password

    def get_invoke_shell(self, hostname, port=22, username='root', password='root!@#456'):
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        try:
            ssh.connect(hostname=hostname, port=port, username=username, password=password)
        except AuthenticationException:
            raise Exception("auth failed user:%s ,passwd:%s" %
                            ('root', ''))
        except SSHException:
            raise Exception("could not connect to host:%s:%s" %
                            ('root', ''))

        print 'host has been connected.......'
        chan = ssh.invoke_shell(term='xterm')
        return chan
