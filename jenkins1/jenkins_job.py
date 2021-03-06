#!/usr/local/miniconda2/bin/python
# _*_ coding:utf-8 _*_
"""
# @Project : docker-dashboard
# @Time    : 2018/10/27 12:58 PM
# @Author  : zhangchengcheng
# @FileName: jenkins_job.py
# @Github  : https://github.com/sweetcczhang
"""
import jenkins
import xml.etree.ElementTree as ET
import time

class JenkinsJob(object):

    def __init__(self, url, username, password):
        self.username = username
        self.password = password
        self.url = url
        self.server = jenkins.Jenkins(self.url, username=self.username, password=self.password)

    # 获取版本
    def get_version(self):
        """
        获取版本
        :return:
        """
        __version = self.server.get_version()
        return __version

    # 获取JOB数量
    def get_job_count(self):
        """
        获取JOB数量
        :return:
        """
        __count = self.server.jobs_count()
        return __count

    # 获取所有JOB
    def get_jobs(self):
        """
        获取所有JOB
        :return:
        """
        __jobs = self.server.get_jobs()
        return __jobs

    # 创建JOB
    def create_job(self, name, config):
        """
        创建JOB
        :param name:
        :param config:
        :return:
        """
        try:
            ET.fromstring(config)
        except Exception as err:
            print('---ILLEGAL XML IN CREATEJOB---')
            print(format(err))
            return 'failure'

        try:
            self.server.create_job(name, config)
            print('Success')
            return 'success'
        except Exception as err:
            print('---ERROR IN CREATEJOB---')
            print(format(err))
            return 'failure'

    # 复制JOB
    def copy_job(self, name, name_new):
        """
        复制JOB
        :param name:
        :param name_new:
        :return:
        """
        try:
            self.server.copy_job(name, name_new)
            print('Success')
        except Exception as err:
            print('---ERROR IN COPYJOB---')
            if self.server.get_job_name(name) == 'None':
                print('---JOB NOT FOUND---')
            elif self.server.get_job_name(name_new) != 'None':
                print('---RENAME NEW JOB---')
            print(format(err))

    # 修改JOB
    def reconfig_job(self, name, config):
        """
        修改JOB
        :param name:
        :param config:
        :return:
        """
        try:
            ET.fromstring(config)
        except Exception as err:
            print('---ILLEGAL XML IN RECONFIGJOB---')
            print(format(err))
            return

        try:
            self.server.reconfig_job(name,config)
            print('Success')
        except Exception as err:
            print('---ERROR IN RECONFIGJOB---')
            print(format(err))

    # 删除JOB
    def delete_job(self, name):
        """
        删除JOB
        :param name:
        :return:
        """
        try:
            self.server.delete_job(name)
            print('Success')
            return 'success'
        except Exception as err:
            print('---ERROR IN DELETEJOB---')
            print(format(err))
            return 'failure'

    # 启用JOB
    def enable_job(self, name):
        """
        启用JOB
        :param name:
        :return:
        """
        try:
            self.server.enable_job(name)
            print('Success')
        except Exception as err:
            print('---ERROR IN ENABLEJOB---')
            print(format(err))

    #
    def disable_job(self, name):
        """
        禁用JOB
        :param name:
        :return:
        """
        try:
            self.server.disable_job(name)
            print('Success')
        except Exception as err:
            print('---ERROR IN DISABLEJOB---')
            print(format(err))

    #
    def get_job_info(self, name):
        """
        获取JOB详细信息
        :param name:
        :return:
        """
        try:
            info = self.server.get_job_info(name)
            return info
        except Exception as err:
            print('---ERROR IN GETJOBINFO---')
            print(format(err))
            return None

    def get_job_config(self, name):
        """
        获取JOB配置
        :param name:
        :return:
        """
        try:
            config = self.server.get_job_config(name)
            return config
        except Exception as err:
            print('---ERROR IN GETJOBCONFIG---')
            print(format(err))

    def build_job(self, name):
        """
        构建Job
        :param name:
        :return:
        """
        try:
            self.server.build_job(name)
            print('Success')
            return 'success'
        except Exception as err:
            print('---ERROR IN BUILDJOB---')
            print(format(err))
            return 'failure'

    def get_build_log(self, name, number):
        """
        获取构建日志
        :param name:
        :param number:
        :return:
        """
        try:
            log = self.server.get_build_console_output(name, number)

            return log
        except Exception as err:
            print('---ERROR IN GET BUILD LOG---')
            print(format(err))

    def get_build_info(self, name, number):
        try:
            info = self.server.get_build_info(name, number)
            return info
        except Exception as e:
            print(format(e))

    def get_views(self):

        return self.server.get_views()


if __name__ == '__main__':
    js = JenkinsJob('http://10.108.210.227:9999', 'admin', 'root!@#456')
    next_build = js.get_job_info(name='sweet123')['nextBuildNumber'] - 1
    build_info = js.get_build_info(name='sweet123', number=next_build)
    print build_info['result']
    print build_info['duration']/1000
    print build_info['displayName']
    print build_info
    print js.get_jobs()

    time_stamp = 1542697674939/1000
    timeArray = time.localtime(time_stamp)
    otherStyleTime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
    print otherStyleTime

'''
jks=jenkinsJob('http://10.108.210.227:9999','admin','root!@#456')
version=jks.getVersion()
count=jks.getJobCount()
job=jks.getJobConfig('empty')
print(version)
'''

'''
server = jenkins1.Jenkins('http://10.108.210.227:9999', username='admin', password='root!@#456')
user = server.get_whoami()
version = server.get_version()
print('Hello %s from Jenkins %s' % (user['fullName'], version))
print(server.jobs_count())
'''