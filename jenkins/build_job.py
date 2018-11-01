#!/usr/local/miniconda2/bin/python
# _*_ coding:utf-8 _*_
"""
# @Project : docker-dashboard
# @Time    : 2018/10/27 12:59 PM
# @Author  : zhangchengcheng
# @FileName: build_job.py
# @Github  : https://github.com/sweetcczhang
"""
import jenkins_job
import jenkins
import xml.dom.minidom

from flask import jsonify, request

jks = jenkins_job.jenkinsJob('http://10.108.210.227:9999', 'admin', 'root!@#456')


def getVersion():
    version = jks.getVersion()
    result = {'version': version}
    return jsonify(result)


def addJobOld():
    if request.method == 'POST':
        jobname = request.POST.get("jobname")
        # TODO根据数据自定义XML
        result = {'result': jks.createJob(jobname, jenkins.EMPTY_CONFIG_XML)}
        return jsonify(result)
    else:
        jobname = request.GET['jobname']
        result = {'result': jks.createJob(jobname, jenkins.EMPTY_CONFIG_XML)}
        return jsonify(result)

    # return HttpResponse(json.dumps(result ), content_type="application/json")


def deleteJob():
    if request.method == 'POST':
        jobname = request.POST.get("jobname")
        result = {'result': jks.deleteJob(jobname)}
        return jsonify(result)
    else:
        jobname = request.GET['jobname']
        result = {'result': jks.deleteJob(jobname)}
        return jsonify(result)


def buildJob():
    if (request.method == 'POST'):
        jobname = request.POST.get("jobname")
        result = {'result': jks.buildJob(jobname)}
        return jsonify(result)
    else:
        jobname = request.GET['jobname']
        result = {'result': jks.buildJob(jobname)}
        return jsonify(result)


def getBuildLog(request):
    if (request.method == 'POST'):
        jobname = request.POST.get("jobname")
        number = int(request.POST.get("number"))
        result = '<pre>' + jks.getBuildLog(jobname, number) + '</pre>'
        return jsonify(result)
    else:
        jobname = request.GET['jobname']
        number = int(request.GET['number'])
        result = '<pre>' + jks.getBuildLog(jobname, number) + '</pre>'
        print(result)
        return jsonify(result)


def getJobXml(request):
    jobname = request.GET['jobname']
    result = jks.getJobConfig(jobname)
    print(result)
    return jsonify(result, content_type='text/xml')


def addJob():
    pass
    # 获取参数 None=null
    if request.method == 'POST':
        jobname = request.values.get('jobname')
        describtion = request.values.get('description')
        gitURL = request.values.get('gitURL')
        credentialsId = request.values.get('credentialsId')
        branches = request.values.get('branches')
        TimerTrigger = request.values.get('TimerTrigger')
        gitlabTrigger = request.values.get('gitlabTrigger')
        script = request.values.get('script')
    else:
        jobname = request.GET('jobname')
        describtion = request.GET('description')
        gitURL = request.GET('gitURL')
        credentialsId = request.GET('credentialsId')
        branches = request.GET('branches')
        TimerTrigger = request.GET('TimerTrigger')
        gitlabTrigger = request.GET('gitlabTrigger')
        script = request.GET('script')

    # 构建XML
    doc = xml.dom.minidom.Document()
    xmlroot = doc.createElement('project')

    xml1actions = doc.createElement('actions')
    xmlroot.appendChild(xml1actions)

    xml1describtion = doc.createElement('description')
    xml1describtion.appendChild(doc.createTextNode(describtion))
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
    xml4url.appendChild(doc.createTextNode(gitURL))
    xml3userconfig.appendChild(xml4url)
    xml4cred = doc.createElement('credentialsId')
    xml4cred.appendChild(doc.createTextNode(credentialsId))
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
    if TimerTrigger != None:
        xml2timetrigger = doc.createElement('hudson.triggers.TimerTrigger')
        xml3spec = doc.createElement('spec')
        xml3spec.appendChild(doc.createTextNode(TimerTrigger))
        xml2timetrigger.appendChild(xml3spec)
        xml1triggers.appendChild(xml2timetrigger)
    if gitlabTrigger != None:
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

    xmlConfig = doc.toxml()
    print(xmlConfig)
    return jsonify(jks.createJob(jobname, doc.toxml()))