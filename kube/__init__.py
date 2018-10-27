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

hostInfo = HostInfo()

deploy = Deployments()

name_space = Namespace()

pods = Pods()

service = Services()

replicas_set = ReplicasSet()

file_create = YamlCreate()
