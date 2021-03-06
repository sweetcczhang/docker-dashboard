#!/usr/local/miniconda2/bin/python
# _*_ coding:utf-8 _*_
"""
# @Project : docker-dashboard
# @Time    : 2018/10/27 2:14 PM
# @Author  : zhangchengcheng
# @FileName: create_from_yaml.py
# @Github  : https://github.com/sweetcczhang
"""
from os import path

from yamls_location_config import YAML_LOC
from kube import basic
from kubernetes.client.rest import ApiException
import yaml
import json


class YamlCreate(basic.Client):

    def create_from_yaml(self, yaml_name):
        """
        从文件中读取yaml文件然后进行解析
        :param yaml_name:
        :return:
        """
        with open(path.join(YAML_LOC, yaml_name)) as f:
            self.get_yaml(f)

    def create_from_json(self, json_name):
        """
        从json文件中读取数据进行解析
        :param json_name:
        :return:
        """
        with open(path.join(YAML_LOC, json_name)) as f:
            self.get_json(f)

    def get_yaml(self, f):
        """
        从前端传来的参数进行数据的解析
        :param f:
        :return:
        """
        dep = yaml.load_all(f)
        try:
            for body in dep:
                print body
                namespace = 'default'
                if body['metadata'].has_key('namespace'):
                    namespace = body['metadata']['namespace']
                if body['kind'] == 'Deployment':
                    self.ext_client.create_namespaced_deployment(namespace=namespace, body=body)

                elif body['kind'] == 'Service':
                    self.v1_client.create_namespaced_service(namespace=namespace, body=body)
                    print body['metadata']['namespace']

                elif body['kind'] == 'Secret':
                    self.v1_client.create_namespaced_secret(namespace=namespace, body=body)

                elif body['kind'] == 'Role':
                    self.role_client.create_namespaced_role(namespace=namespace, body=body)

                elif body['kind'] == 'RoleBinding':
                    self.role_client.create_namespaced_role_binding(namespace=namespace, body=body)

                elif body['kind'] == 'ServiceAccount':
                    self.v1_client.create_namespaced_service_account(namespace=namespace, body=body)
                elif body['kind'] == 'HorizontalPodAutoscaler':
                    namespace = 'default'
                    self.auto_client.create_namespaced_horizontal_pod_autoscaler(namespace=namespace, body=body)
                else:
                    print('test')
        except ApiException as e:
            print e
        except Exception as e:
            print e

    def get_json(self, f):
        """
        从前端传来的参数进行数据解析
        :param f:
        :return:
        """
        body = json.load(f)
        if body['kind'] == 'Deployment':
            self.ext_client.create_namespaced_deployment(namespace=body['metadata']['namespace'], body=body)

        elif body['kind'] == 'Service':
            self.v1_client.create_namespaced_service(namespace=body['metadata']['namespace'], body=body)
            print body['metadata']['namespace']

        elif body['kind'] == 'Secret':
            self.v1_client.create_namespaced_secret(namespace=body['metadata']['namespace'], body=body)

        elif body['kind'] == 'Role':
            self.role_client.create_namespaced_role(namespace=body['metadata']['namespace'], body=body)

        elif body['kind'] == 'RoleBinding':
            self.role_client.create_namespaced_role_binding(namespace=body['metadata']['namespace'], body=body)

        elif body['kind'] == 'ServiceAccount':
            self.v1_client.create_namespaced_service_account(namespace=body['metadata']['namespace'], body=body)


if __name__ == '__main__':

    test = {}
    test['kind'] = 'Deployment'
    print test.has_key('a')
    y = YamlCreate()
    y.create_from_yaml('dashboard.yaml')
    #y.create_from_json('test.json')
