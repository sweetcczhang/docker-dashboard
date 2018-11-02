#!/usr/local/miniconda2/bin/python
# _*_ coding:utf-8 _*_
"""
# @Project : docker-dashboard
# @Time    : 2018/11/2 5:42 PM
# @Author  : zhangchengcheng
# @FileName: create_image.py
# @Github  : https://github.com/sweetcczhang
"""
import os
import confHarbor


def image_build(image_name, version):
    # if request.method == 'POST':
    #     imageName = request.POST.get("imageName")
    #     version = request.POST.get("version")
    #     dockerfile = request.FILES.get("dockerfile")
    #     print(imageName)
    #     print(version)
        # print(dockerfile.read())
        # jobname=request.POST.get("jobname")

    # else:
    #     # jobname=request.GET['jobname']
    #     print('')
    # f = open('Dockerfile', 'w')
    # f.write(dockerfile.read())
    # f.close()

    command = 'docker login ' + confHarbor.HARBOR_URL+' -p ' + confHarbor.HARBOR_PASSWORD+' -u ' +\
              confHarbor.HARBOR_USERNAME
    os.system(command)

    command = 'docker build -t '+confHarbor.HARBOR_URL+'/library/' + image_name + ':' + version + ' .'
    print(command)
    output = os.popen(command)
    result = output.read()
    command = 'docker push ' + confHarbor.HARBOR_URL + '/library/' + image_name + ':' + version
    output = os.popen(command)
    result += output.read()
    print(result)
    return result
