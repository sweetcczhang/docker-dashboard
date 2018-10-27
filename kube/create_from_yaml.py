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
import yaml
import json


class YamlCreate(basic.Client):

    def create_from_yaml(self, yaml_name):

        with open(path.join(YAML_LOC, yaml_name)) as f:

            dep = yaml.load_all(f)

            for body in dep:

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

    def create_from_json(self, json_name):

        with open(path.join(YAML_LOC, json_name)) as f:

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
    y = YamlCreate()
    y.create_from_yaml('dashboard.yaml')
    y.create_from_json('test.json')
