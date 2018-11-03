#!/usr/local/miniconda2/bin/python
# _*_ coding:utf-8 _*_
"""
# @Time   : 2018/7/21 15:59
# @Author : 张城城
"""
from jenkins_job import JenkinsJob
import mysql.connector
import db_config
jks = JenkinsJob('http://10.108.210.227:9999', 'admin', 'root!@#456')


def connect_db():
    db = mysql.connector.connect(user=db_config.USER, passwd=db_config.PASSWORD, database=db_config.DATABASE,
                                 host=db_config.HOST, port=db_config.PORT)

    return db
