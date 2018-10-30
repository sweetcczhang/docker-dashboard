#!/usr/local/miniconda2/bin/python
# _*_ coding:utf-8 _*_
"""
# @Time   : 2018/7/11 23:11
# @Author : 张城城
"""

from kube.kube_hostInfo import HostInfo
from kube.kube_deployment import Deployments
from kube.kube_namespace import Namespace
from kube.kube_pod import Pods
from kube.kube_service import Services
from kube.kube_replicas_set import ReplicasSet

from kube.create_from_yaml import YamlCreate

from kube.kube_autoscale import AutoScale

"""
获取主机相关的信息
"""
hostInfo = HostInfo()
"""
获取deployment相关的信息
"""
deploys = Deployments()
"""
获取namespace相关的信息
"""
name_space = Namespace()
"""
获取pod相关的信息
"""
pods_client = Pods()
"""
获取service相关的信息
"""
service_client = Services()
"""
获取replicas相关的信息
"""
replicas_client = ReplicasSet()
"""
通过上传yaml文件或者json文件构建应用
"""
file_create = YamlCreate()
"""
获取自动获取相关的内容
"""
scale_client = AutoScale()
