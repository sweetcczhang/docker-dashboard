#!/usr/local/miniconda2/bin/python
# _*_ coding:utf-8 _*_
"""
# @Project : docker-dashboard
# @Time    : 2018/10/27 12:59 PM
# @Author  : zhangchengcheng
# @FileName: build_job.py
# @Github  : https://github.com/sweetcczhang
"""

from jenkins1 import jks
import jenkins1
import xml.dom.minidom
import time

from flask import jsonify, request, Blueprint

jenkin = Blueprint('build_job', __name__)


@jenkin.route('/getJobInfo', methods=['GET', 'POST'])
def get_job_info():
    return_model = {}
    name = request.values.get(key='name')
    try:
        info = jks.get_job_info(name=name)
        return_model['retCode'] = 200
        return_model['retDesc'] = 'success'
        return_model['data'] = info
    except Exception as e:
        print e
        return_model['retCode'] = 500
        return_model['retDesc'] = '获取%s信息失败', name

    return jsonify(return_model)


@jenkin.route('/getVersion', methods=['GET', 'POST'])
def get_version():
    return_model = {}
    try:
        version = jks.getVersion()
        return_model['retCode'] = 200
        return_model['retDesc'] = 'success'
        return_model['data'] = version
    except Exception as e:
        print e
        return_model['retCode'] = 500
        return_model['retDesc'] = '接口调用错误'

    return jsonify(return_model)


@jenkin.route('/getAllJob', methods=['GET', 'POST'])
def get_all_job():
    return_model = {}
    try:

        all_job = jks.get_jobs()
        data = []
        for job in all_job:
            next_build = jks.get_job_info(name=job['name'])['nextBuildNumber'] - 1
            if next_build == 0:
                temp = {'name': job['name'], 'result': 'notBuild', 'buildTime': 'notBuild',
                        'duration': 'notBuild', 'builds': 'notBuild', 'branches': '/master'}
            else:
                build_info = jks.get_build_info(name=job['name'], number=next_build)
                time_stamp = build_info['timestamp'] / 1000
                timeArray = time.localtime(time_stamp)
                otherStyleTime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
                temp = {'name': job['name'], 'result': build_info['result'], 'buildTime': otherStyleTime,
                        'duration': build_info['duration']/1000, 'builds': build_info['displayName'],
                        'branches': '/master'}
            data.append(temp)

        # db = jenkins1.connect_db()
        # cur = db.cursor()
        # sql = "SELECT * FROM jenkins"
        # cur.execute(sql)
        # results = cur.fetchall()
        # data = {}
        # for r in results:
        #     temp = {'jobName': r[1], 'description': r[2], 'gitUrl': r[3], 'branches': r[5], 'timeTrigger': r[6],
        #             'gitlabTrigger': r[7], 'username': r[8], 'password': r[9]}
        #     data[r[1]] = temp
        return_model['retCode'] = 200
        return_model['retDesc'] = 'success'
        return_model['data'] = data
    except Exception as e:
        print e
        return_model['retCode'] = 500
        return_model['retDesc'] = '获取任务列表失败'
    # finally:
    #     db.close()
    return jsonify(return_model)


@jenkin.route('/deleteJob', methods=['GET', 'POST'])
def delete_job():
    return_model = {}
    job_name = request.values.get(key='jobName')
    try:
        result = jks.delete_job(name=job_name)
        db = jenkins1.connect_db()
        cur = db.cursor()
        sql = "DELETE FROM jenkins WHERE job_name='%s'" % (job_name)
        cur.execute(sql)
        db.commit()
        return_model['retCode'] = 200
        return_model['retDesc'] = 'success'
        return_model['data'] = result
    except Exception as e:
        print e
        db.rollback()
        return_model['retCode'] = 500
        return_model['retDesc'] = '删除失败'
    finally:
        db.close()
    return jsonify(return_model)


@jenkin.route('/buildJob', methods=['GET', 'POST'])
def build_job():
    job_name = request.values.get('jobName', default=None)
    return_model = {}
    try:
        result = jks.build_job(name=job_name)
        return_model['retCode'] = 200
        return_model['retDesc'] = 'success'
        return_model['data'] = result
    except Exception as e:
        print e
        return_model['retCode'] = 500
        return_model['retDesc'] = '构建失败'
    return jsonify(return_model)


@jenkin.route('/getBuildJob', methods=['GET', 'POST'])
def get_build_log():
    return_model = {}
    try:
        job_name = request.values.get("jobname")
        number = int(request.values.get("number", default=1))
        result = jks.get_build_log(name=job_name, number=number)
        return_model['retCode'] = 200
        return_model['retDesc'] = 'success'
        return_model['data'] = result
    except Exception as e:
        print e
        return_model['retDesc'] = '获取构建日志失败'
        return_model['retCode'] = 500
    return jsonify(return_model)


@jenkin.route('/getJobXML', methods=['GET', 'POST'])
def get_job_xml():
    return_model = {}
    job_name = request.values.get(key='jobName')
    try:
        result = jks.get_job_config(name=job_name)
        print(result)
        return_model['retCode'] = 200
        return_model['retDesc'] = 'success'
        return_model['data'] = result
    except Exception as e:
        print e
        return_model['retCode'] = 500
        return_model['retDesc'] = '获取%s的xml失败', job_name

    return jsonify(return_model)


@jenkin.route('/reConfigJob', methods=['GET', 'POST'])
def re_config_job():
    # 获取参数 None=null
    job_name = request.values.get(key='jobname')
    description = request.values.get(key='description', default=job_name)
    git_url = request.values.get(key='gitURL')
    credentials_id = request.values.get(key='credentialsId', default='')
    branches = request.values.get(key='branches')
    timer_trigger = request.values.get(key='TimerTrigger')
    gitlab_trigger = request.values.get(key='gitlabTrigger')
    script = request.values.get(key='script')
    username = request.values.get(key='username')
    password = request.values.get(key='password')
    return_model = {}

    # 构建XML
    doc = build_xml(description=description, git_url=git_url, credentials_id=credentials_id, branches=branches,
                    timer_trigger=timer_trigger, gitlab_trigger=gitlab_trigger, script=script)
    try:
        jks.reconfig_job(job_name=job_name, config=doc.toxml())
        db = jenkins1.connect_db()
        cur = db.cursor()
        sql = "UPDATE jenkins SET description='%s', git_url='%s', credentials_id='%s', branches='%s'," \
              " timer_trigger='%s', gitlab_trigger='%s', script='%s',username='%s', password='%d' " \
              "WHERE job_name='%s'" % (description, git_url, credentials_id, branches, timer_trigger, gitlab_trigger,
                                       script, username, password)
        cur.execute(sql)
        db.commit()
        return_model['retCode'] = 200
        return_model['retDesc'] = 'success'

    except Exception as e:
        print e
        db.rollback()
        return_model['retCode'] = 500
        return_model['retDesc'] = '更新失败'
    finally:
        db.close()

    return jsonify(return_model)


@jenkin.route('/addJob', methods=['GET', 'POST'])
def add_job():
    # 获取参数 None=null
    job_name = request.values.get(key='jobname')
    description = request.values.get(key='description', default=job_name)
    git_url = request.values.get(key='gitURL')
    credentials_id = request.values.get(key='credentialsId', default='04ea4e1c-20aa-4223-abef-d83f7c46e8d2')
    branches = request.values.get(key='branches')
    timer_trigger = request.values.get(key='TimerTrigger')
    gitlab_trigger = request.values.get(key='gitlabTrigger')
    script = request.values.get(key='script')
    username = request.values.get(key='username')
    password = request.values.get(key='password')
    return_model = {}

    # 构建XML
    print 'start build xml'
    doc = build_xml(description=description, git_url=git_url, credentials_id=credentials_id, branches=branches,
                    timer_trigger=timer_trigger, gitlab_trigger=gitlab_trigger, script=script)

    xml_config = doc.toxml()
    print(xml_config)
    try:
        result = jks.create_job(job_name, doc.toxml())
        return_model['retCode'] = 200
        return_model['retDesc'] = 'success'
        return_model['data'] = result
        db = jenkins1.connect_db()
        cur = db.cursor()
        sql = "INSERT INTO jenkins(job_name,description,git_url,credentials_id,branches,timer_trigger," \
              "gitlab_trigger,script,username,password) VALUES('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')"\
              % (job_name, description, git_url, credentials_id, branches, timer_trigger, gitlab_trigger, script,
                 username, password)

        cur.execute(sql)
        db.commit()
    except Exception as e:
        print e
        db.rollback()
        return_model['retCode'] = 500
        return_model['retDesc'] = '创建job失败'
    finally:
        db.close()
    return jsonify(return_model)


def build_xml(description, git_url, credentials_id, branches, timer_trigger, gitlab_trigger, script):
    doc = xml.dom.minidom.Document()
    xmlroot = doc.createElement('project')

    xml1actions = doc.createElement('actions')
    xmlroot.appendChild(xml1actions)

    xml1describtion = doc.createElement('description')
    xml1describtion.appendChild(doc.createTextNode(description))
    xmlroot.appendChild(xml1describtion)

    xml1keepD = doc.createElement('keepDenpendencies')
    xml1keepD.appendChild(doc.createTextNode('false'))
    xmlroot.appendChild(xml1keepD)

    xml1properties = doc.createElement('properties')
    xml2gitplugin = doc.createElement('com.dabsquared.gitlabjenkins.connection.GitLabConnectionProperty')
    xml2gitplugin.setAttribute('plugin', 'gitlab-plugin@1.5.9')
    xml3gitcon = doc.createElement('gitLabConnection')
    xml2gitplugin.appendChild(xml3gitcon)
    xml1properties.appendChild(xml2gitplugin)

    xml1scm = doc.createElement('scm')
    xml1scm.setAttribute('class', 'hudson.plugins.git.GitSCM')
    xml1scm.setAttribute('plugin', 'git@3.9.1')
    xml2configver = doc.createElement('configVersion')
    xml2configver.appendChild(doc.createTextNode('2'))
    xml1scm.appendChild(xml2configver)
    xml2userconfig = doc.createElement('userRemoteConfigs')
    xml3userconfig = doc.createElement('hudson.plugins.git.UserRemoteConfig')
    xml4url = doc.createElement('url')
    xml4url.appendChild(doc.createTextNode(git_url))
    xml3userconfig.appendChild(xml4url)
    xml4cred = doc.createElement('credentialsId')
    xml4cred.appendChild(doc.createTextNode(credentials_id))
    xml3userconfig.appendChild(xml4cred)
    xml2userconfig.appendChild(xml3userconfig)
    xml1scm.appendChild(xml2userconfig)
    xml2branches = doc.createElement('branches')
    xml3branches = doc.createElement('hudson.plugins.git.BranchSpec')
    xml4name = doc.createElement('name')
    xml4name.appendChild(doc.createTextNode(branches))
    xml3branches.appendChild(xml4name)
    xml2branches.appendChild(xml3branches)
    xml1scm.appendChild(xml2branches)
    xml2dos = doc.createElement('doGenerateSubmoduleConfigurations')
    xml2dos.appendChild(doc.createTextNode('false'))
    xml1scm.appendChild(xml2dos)
    xml2submodule = doc.createElement('submoduleCfg')
    xml2submodule.setAttribute('class', 'list')
    xml1scm.appendChild(xml2submodule)
    xml2extension = doc.createElement('extensions')
    xml1scm.appendChild(xml2extension)
    xmlroot.appendChild(xml1scm)

    xml1canRoam = doc.createElement('canRoam')
    xml1canRoam.appendChild(doc.createTextNode('true'))
    xmlroot.appendChild(xml1canRoam)

    xml1disabled = doc.createElement('disabled')
    xml1disabled.appendChild(doc.createTextNode('false'))
    xmlroot.appendChild(xml1disabled)

    xml1blockBD = doc.createElement('blockBuildWhenDownstreamBuilding')
    xml1blockBD.appendChild(doc.createTextNode('false'))
    xmlroot.appendChild(xml1blockBD)

    xml1blockBU = doc.createElement('blockBuildWhenUpstreamBuilding')
    xml1blockBU.appendChild(doc.createTextNode('false'))
    xmlroot.appendChild(xml1blockBU)

    xml1triggers = doc.createElement('triggers')
    if timer_trigger is not None:
        xml2timetrigger = doc.createElement('hudson.triggers.TimerTrigger')
        xml3spec = doc.createElement('spec')
        xml3spec.appendChild(doc.createTextNode(timer_trigger))
        xml2timetrigger.appendChild(xml3spec)
        xml1triggers.appendChild(xml2timetrigger)
    if gitlab_trigger is not None:
        xml2gittrigger = doc.createElement('com.dabsquared.gitlabjenkins.GitLabPushTrigger')
        xml2gittrigger.setAttribute('plugin', 'gitlab-plugin@1.5.9')
        xml3spec2 = doc.createElement('spec')
        xml2gittrigger.appendChild(xml3spec2)
        xml3triggeronpush = doc.createElement('triggerOnPush')
        xml3triggeronpush.appendChild(doc.createTextNode('true'))
        xml2gittrigger.appendChild(xml3triggeronpush)
        xml3triggeronmerge = doc.createElement('triggerOnMergeRequest')
        xml3triggeronmerge.appendChild(doc.createTextNode('true'))
        xml2gittrigger.appendChild(xml3triggeronmerge)
        xml3triggeronpipe = doc.createElement('triggerOnPipelineEvent')
        xml3triggeronpipe.appendChild(doc.createTextNode('false'))
        xml2gittrigger.appendChild(xml3triggeronpipe)
        xml3triggeronaccept = doc.createElement('triggerOnAcceptedMergeRequest')
        xml3triggeronaccept.appendChild(doc.createTextNode('false'))
        xml2gittrigger.appendChild(xml3triggeronaccept)
        xml3triggeronclose = doc.createElement('triggerOnClosedMergeRequest')
        xml3triggeronclose.appendChild(doc.createTextNode('false'))
        xml2gittrigger.appendChild(xml3triggeronclose)
        xml3triggeronapprove = doc.createElement('triggerOnApprovedMergeRequest')
        xml3triggeronapprove.appendChild(doc.createTextNode('true'))
        xml2gittrigger.appendChild(xml3triggeronapprove)
        xml3triggeropenmerge = doc.createElement('triggerOpenMergeRequestOnPush')
        xml3triggeropenmerge.appendChild(doc.createTextNode('never'))
        xml2gittrigger.appendChild(xml3triggeropenmerge)
        xml3triggeronnote = doc.createElement('triggerOnNoteRequest')
        xml3triggeronnote.appendChild(doc.createTextNode('true'))
        xml2gittrigger.appendChild(xml3triggeronnote)
        xml3noteregex = doc.createElement('noteRegex')
        xml3noteregex.appendChild(doc.createTextNode('Jenkins please retry a build'))
        xml2gittrigger.appendChild(xml3noteregex)
        xml3ciskip = doc.createElement('ciSkip')
        xml3ciskip.appendChild(doc.createTextNode('true'))
        xml2gittrigger.appendChild(xml3ciskip)
        xml3skipwork = doc.createElement('skipWorkInProgressMergeRequest')
        xml3skipwork.appendChild(doc.createTextNode('true'))
        xml2gittrigger.appendChild(xml3skipwork)
        xml3setbuild = doc.createElement('setBuildDescription')
        xml3setbuild.appendChild(doc.createTextNode('true'))
        xml2gittrigger.appendChild(xml3setbuild)
        xml3branchf = doc.createElement('branchFilterType')
        xml3branchf.appendChild(doc.createTextNode('All'))
        xml2gittrigger.appendChild(xml3branchf)
        xml3includebranch = doc.createElement('includeBranchesSpec')
        xml2gittrigger.appendChild(xml3includebranch)
        xml3excludebranch = doc.createElement('excludeBranchesSpec')
        xml2gittrigger.appendChild(xml3excludebranch)
        xml3targetbranch = doc.createElement('targetBranchRegex')
        xml2gittrigger.appendChild(xml3targetbranch)
        xml3secrettoken = doc.createElement('secretToken')
        xml3secrettoken.appendChild(doc.createTextNode('{AQAAABAAAAAQcPwSJtnHrGEMCC9SDN/8lhlhxA5IKmcIJl1+E2Hkm5o=}'))
        xml2timetrigger.appendChild(xml3secrettoken)
        xml3pending = doc.createElement('pendingBuildName')
        xml2gittrigger.appendChild(xml3pending)
        xml3cancelpending = doc.createElement('cancelPendingBuildsOnUpdate')
        xml3cancelpending.appendChild(doc.createTextNode('false'))
        xml2gittrigger.appendChild(xml3cancelpending)
        xml1triggers.appendChild(xml2gittrigger)
    xmlroot.appendChild(xml1triggers)

    xml1concurrentBuild = doc.createElement('concurrentBuild')
    xml1concurrentBuild.appendChild(doc.createTextNode('false'))
    xmlroot.appendChild(xml1concurrentBuild)

    xml1builders = doc.createElement('builders')
    xml2shell = doc.createElement('hudson.tasks.Shell')
    xml3command = doc.createElement('command')
    xml3command.appendChild(doc.createTextNode(script))
    xml2shell.appendChild(xml3command)
    xml1builders.appendChild(xml2shell)
    xmlroot.appendChild(xml1builders)

    xml1publishers = doc.createElement('publishers')
    xmlroot.appendChild(xml1publishers)

    xml1buildWrappers = doc.createElement('buildWrappers')
    xmlroot.appendChild(xml1buildWrappers)
    doc.appendChild(xmlroot)
    print doc.toxml()
    return doc
