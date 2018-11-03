#!/usr/local/miniconda2/bin/python
# _*_ coding:utf-8 _*_
"""
# @Time   : 2018/7/22 16:44
# @Author : 张城城
"""
from __future__ import print_function
import logging


from harbor import utils
from harbor.rest import harbor as harbor_client

from flask import request, jsonify, Blueprint

# from jenkins1 import create_image as build

logger = logging.getLogger(__name__)

harbors = Blueprint('restapi', __name__)


def do_search():
    """Search for projects and repositories."""
    return_model = {}
    query = request.args.get('query')

    if not query or query is None:
        return_model['retCode'] = 500
        return_model['retDesc'] = 'fail'
        return_model['reason'] = '請填寫參數'
        return_model['data'] = None
        return jsonify(return_model)

    data = harbor_client.searcher.search(query)
    logger.info("Find %d Projects: " % len(data['project']))
    logger.info("Find %d Repositories: " % len(data['repository']))
    return jsonify(return_model)


# @harbors.route('/buildImage', methods=['GET', 'POST'])
# def build_image_from_file():
#     return_model = {}
#     image_name = request.values.get(key='imageName', default=None)
#     label = request.values.get(key='label', default='latest')
#     dockerfile = request.files['dockerfile']
#     with open('Dockerfile', 'w') as f:
#         f.write(dockerfile.read())
#         f.close()
#     try:
#         result = build.image_build(image_name=image_name, version=label)
#         return_model['retDesc'] = 'success'
#         return_model['retCode'] = 200
#         return_model['data'] = result
#     except Exception as f:
#         return_model['retDesc'] = '镜像构建失败'
#         return_model['retCode'] = 500
#         print(f)
#     return jsonify(return_model)


@harbors.route('/buildImageStr', methods=['POST'])
def build_image_from_str():
    return_model = {}
    image_name = request.values.get(key='imageName', default=None)
    label = request.values.get(key='label', default='latest')
    dockerfile = request.values.get('dockerfile', default=None)
    with open('Dockerfile', 'w') as f:
        f.write(dockerfile.read())
        f.close()
    try:
        result = build.image_build(image_name=image_name, version=label)
        return_model['retDesc'] = 'success'
        return_model['retCode'] = 200
        return_model['data'] = result
    except Exception as f:
        return_model['retDesc'] = '镜像构建失败'
        return_model['retCode'] = 500
        print(f)
    return jsonify(return_model)


@harbors.route('/getHarborLogs', methods=['GET', 'POST'])
def get_harbor_logs():
    return_model = {}
    try:
        logs = harbor_client.logs.list()
        return_model['retCode'] = 200
        return_model['retDesc'] = 'success'
        return_model['data'] = {'length': len(logs), 'logsList': logs}
    except Exception as e:
        print(e)
        return_model['retCode'] = 500
        return_model['retDesc'] = ' 请求harbor操作日志失败'
    return jsonify(return_model)

    # print (logs)
    # for log in logs:
    #     repo = log['repo_name']
    #     tag = None
    #     if log['repo_tag'] != 'N/A':
    #         tag = log['repo_tag']
    #     if tag:
    #         repo += ":%s" % tag
    #     log['repository'] = repo
    # fields = ['log_id', 'op_time', 'username',
    #           'project_id', 'operation', 'repository']
    # utils.print_list(logs, fields)


@harbors.route('/showProjectDetail')
def show_project_detail():
    """Show specific repository detail information."""
    return_model = {}

    project = request.values.get('project', harbor_client.client.project)
    repo = request.values.get('repository')
    tag_index = repo.find(':')
    if tag_index != -1:
        tag = repo[tag_index + 1:]
        repo = repo[:tag_index]
    else:
        tag = "latest"
    if repo.find('/') == -1:
        repo = "library/" + repo
    repos = harbor_client.repositories.list(project)
    found_repo = None
    for r in repos:
        if r['name'] == repo:
            found_repo = r
            break
    if not found_repo:
        print("Image '%s' not found." % repo)
        return_model['retCode'] = 500
        return_model['retDesc'] = 'fail'
        return_model['reason'] = "Image" + repo + "not found"
        return jsonify(return_model)
    tags = harbor_client.repositories.list_tags(found_repo['name'])
    found_tag = None
    for t in tags:
        if t['name'] == tag:
            found_tag = t
            break
    if not found_tag:
        print("Image '%s' with tag '%s' not found." % (repo, tag))
        return_model['retCode'] = 500
        return_model['retDesc'] = 'fail'
        return_model['reason'] = "Image" + repo + "with tag" + tag + "not found"
        return jsonify(return_model)
    for key in found_tag:
        found_repo['tag_' + key] = found_tag[key]

    return_model['retCode'] = 200
    return_model['retDesc'] = 'success'
    return_model['data'] = found_repo
    return jsonify(return_model)
    # utils.print_dict(found_repo)


@harbors.route('/list')
def get_image_list():
    """查詢鏡像倉庫的鏡像列表"""
    project = request.args.get('project', default=1)
    #project = 1
    repositories = harbor_client.repositories.list(project)
    return_model = {}

    data = []
    for repo in repositories:
        tags = harbor_client.repositories.list_tags(repo['name'])
        for tag in tags:
            item = repo.copy()
            manifest = harbor_client.repositories.get_manifests(item['name'],
                                                     tag['name'])
            size = 0

            for layer in manifest['manifest']['layers']:
                size += layer['size']
            item['size'] = str(size/(1024*1024)) + 'Mi'

            if tag['name'] != 'latest':
                item['name'] = repo['name'] + ":" + tag['name']
            item['labels'].append(tag['name'])
            data.append(item)

    result = {'length': len(data), 'images': data}
    return_model['retCode'] = 200
    return_model['retDesc'] = 'success'
    return_model['data'] = result

    fields = [
        "name", 'project_id', 'size',
        "tags_count", "star_count", "pull_count",
        "update_time"
    ]
    utils.print_list(data, fields)
    return jsonify(return_model)


if __name__ == "__main__":
    # get_image_list()
    get_harbor_logs()
