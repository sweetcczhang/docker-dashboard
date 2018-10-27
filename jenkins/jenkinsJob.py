# _*_ coding:utf-8 _*_

import jenkins
import xml.etree.ElementTree as ET


class jenkinsJob:
    def __init__(self, url, username, password):
        self.username = username
        self.password = password
        self.url = url
        self.server = jenkins.Jenkins(self.url, username=self.username, password=self.password)

    #获取版本
    def getVersion(self):
        __version = self.server.get_version()
        return __version

    #获取JOB数量
    def getJobCount(self):
        __count = self.server.jobs_count()
        return __count

    #获取所有JOB    
    def getJobs(self):
        __jobs = self.server.get_jobs()
        return __jobs

    #创建JOB
    def createJob(self, name, config):
        try:
            ET.fromstring(config)
        except Exception as err:
            print('---ILLEGAL XML IN CREATEJOB---')
            print(format(err))
            return 'failure'

        try:
            self.server.create_job(name,config)
            print('Success')
            return 'success'
        except Exception as err:
            print('---ERROR IN CREATEJOB---')
            print(format(err))
            return 'failure'

    #复制JOB
    def copyJob(self,name,name_new):
        try:
            self.server.copy_job(name,name_new)
            print('Success')
        except Exception as err:  
            print('---ERROR IN COPYJOB---')
            if self.server.get_job_name(name) == 'None':
                print('---JOB NOT FOUND---')
            elif self.server.get_job_name(name_new) != 'None':
                print('---RENAME NEW JOB---')
            print(format(err))

    #修改JOB
    def reconfigJob(self,name,config):
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

    #删除JOB
    def deleteJob(self,name):
        try:
            self.server.delete_job(name)
            print('Success')
            return 'success'
        except Exception as err:            
            print('---ERROR IN DELETEJOB---')    
            print(format(err))
            return 'failure'

    #启用JOB
    def enableJob(self,name):
        try:
            self.server.enable_job(name)
            print('Success')
        except Exception as err:
            print('---ERROR IN ENABLEJOB---')
            print(format(err))

    #禁用JOB
    def disableJob(self,name):
        try:
            self.server.disable_job(name)
            print('Success')
        except Exception as err:
            print('---ERROR IN DISABLEJOB---')
            print(format(err))

    #获取JOB详细信息
    def getJobInfo(self,name):
        try:
            info=self.server.get_job_info(name)
            return info 
        except Exception as err:
            print('---ERROR IN GETJOBINFO---')
            print(format(err))

    #获取JOB配置
    def getJobConfig(self, name):
        try:
            config=self.server.get_job_config(name)
            return config
        except Exception as err:
            print('---ERROR IN GETJOBCONFIG---')
            print(format(err))

    #构建Job
    def buildJob(self,name):
        try:
            self.server.build_job(name)
            print('Success')
            return 'success'
        except Exception as err:
            print('---ERROR IN BUILDJOB---')
            print(format(err))
            return 'failure'

    #获取构建日志
    def getBuildLog(self,name,number):
        try:
            log=self.server.get_build_console_output(name, number)
            return log
        except Exception as err:
            print('---ERROR IN GETBUILDLOG---')
            print(format(err))
'''
jks=jenkinsJob('http://10.108.210.227:9999','admin','root!@#456')
version=jks.getVersion()
count=jks.getJobCount()
job=jks.getJobConfig('empty')
print(version)
'''
'''
server = jenkins.Jenkins('http://10.108.210.227:9999', username='admin', password='root!@#456')
user = server.get_whoami()
version = server.get_version()
print('Hello %s from Jenkins %s' % (user['fullName'], version))
print(server.jobs_count())
'''