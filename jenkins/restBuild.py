#!/usr/local/miniconda2/bin/python
# _*_ coding:utf-8 _*_
"""
# @Project : docker-dashboard
# @Time    : 2018/11/2 11:33 PM
# @Author  : zhangchengcheng
# @FileName: restBuild.py
# @Github  : https://github.com/sweetcczhang
"""
from flask import jsonify, request, Blueprint

jenkin = Blueprint('restBuild', __name__)


def build_job():
    return_model = {}

    return jsonify(return_model)