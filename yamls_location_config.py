#!/usr/local/miniconda2/bin/python
# _*_ coding:utf-8 _*_
"""
# @Project : docker-dashboard
# @Time    : 2018/10/27 4:05 PM
# @Author  : zhangchengcheng
# @FileName: yamls_location_config.py
# @Github  : https://github.com/sweetcczhang
"""
import os

APP_ROOT = os.path.dirname(os.path.abspath(__file__))

YAML_LOC = os.path.join(APP_ROOT, "yamls")

ALLOWED_EXTENSIONS = set(['yaml', 'json'])


def allowed_file(file_name):
    return '.' in file_name and file_name.rspplit('.', 1)[1] in ALLOWED_EXTENSIONS


print YAML_LOC
print APP_ROOT
