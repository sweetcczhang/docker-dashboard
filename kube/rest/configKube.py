#!/usr/local/miniconda2/bin/python
# _*_ coding:utf-8 _*_

"""
#配置 kubernetes的访问凭证
# @Time   : 2018/7/21 15:58
# @Author : 张城城
"""

from kubernetes import client, config


def config_kube():
    """
    配置访问凭证
    :return:
    """
    config.load_kube_config(config_file='/root/zcc/hello/config')


def get_core_v1_api():
    """
    获取CoreV1Api
    :return:
    """
    config_kube()
    v1 = client.CoreV1Api()
    return v1


def get_extensions():
    """
    获取 ExtensionsV1betaApi
    :return:
    """
    config_kube()
    extension = client.ExtensionsV1beta1Api()
    return extension
