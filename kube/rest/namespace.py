#!/usr/local/miniconda2/bin/python
# _*_ coding:utf-8 _*_
"""
# @Project : docker-dashboard
# @Time    : 2018/11/29 4:48 PM
# @Author  : zhangchengcheng
# @FileName: namespace.py
# @Github  : https://github.com/sweetcczhang
"""

from flask import Blueprint, jsonify, request
from kube import name_space

space = Blueprint('namespace', __name__)


@space.route('/getNamespace', methods=['GET', 'POST'])
def get_namespace():
    return_model = {}

    try:
        name_list = name_space.list_all_namespace()
        if len(name_list) == 0:
            raise Exception('')

        return_model['retCode'] = 200
        return_model['retDesc'] = 'success'
        return_model['data'] = name_list

    except Exception as e:
        print e
        return_model['retCode'] = 500
        return_model['retDesc'] = '查询命名空间失败'

    return jsonify(return_model)


@space.route('/createSpace', methods=['GET', 'POST'])
def create_namespace():
    return_model = {}

    return jsonify(return_model)
