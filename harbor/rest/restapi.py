#!/usr/local/miniconda2/bin/python
# _*_ coding:utf-8 _*_
"""
# @Time   : 2018/7/22 16:44
# @Author : 张城城
"""
from __future__ import print_function
import logging


from harbor import utils
from harbor import rest

import confHarbor
from flask import request, jsonify, Blueprint

logger = logging.getLogger(__name__)

harbors = Blueprint('restapi', __name__)


@harbors.route('/showProjectDetail')
def show_project_detail():
    """Show specific repository detail infomation."""
    return_model = {}
    harbor = rest.get_harbor_client(api_version=None, username=confHarbor.HARBOR_USERNAME,
                                    password=confHarbor.HARBOR_PASSWORD,
                                    project=confHarbor.HARBOR_PROJECT, base_url=confHarbor.HARBOR_URL)
    project = request.args.get('project', harbor.client.project)
    repo = request.args.get('repository')
    tag_index = repo.find(':')
    if tag_index != -1:
        tag = repo[tag_index + 1:]
        repo = repo[:tag_index]
    else:
        tag = "latest"
    if repo.find('/') == -1:
        repo = "library/" + repo
    repos = harbor.repositories.list(project)
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
    tags = harbor.repositories.list_tags(found_repo['name'])
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
    utils.print_dict(found_repo)


@harbors.route('/deleteUser', methods={'POST', 'GET'})
def delete_user():
    username = request.args.get('username', None)
    return_model = {}
    harbor = rest.get_harbor_client(api_version=None, username=confHarbor.HARBOR_USERNAME,
                                    password=confHarbor.HARBOR_PASSWORD,
                                    project=confHarbor.HARBOR_PROJECT, base_url=confHarbor.HARBOR_URL)
    if harbor.users.is_id(username):
        id = username
    else:
        id = harbor.users.get_id_by_name(username)
    harbor.users.delete(id)
    print("Delete user '%s' successfully." % username)

    return_model['retCode'] = 200
    return_model['retDesc'] = 'success'
    return_model['data'] = None
    return jsonify(return_model)


@harbors.route('/createUser', methods={'POST', 'GET'})
def create_user():

    username = request.form('username')
    password = request.form('password')
    email = request.form('email')
    realname = request.form('realname')
    comment = request.form('comment')
    return_model = {}
    harbor = rest.get_harbor_client(api_version=None, username=confHarbor.HARBOR_USERNAME,
                                    password=confHarbor.HARBOR_PASSWORD,
                                    project=confHarbor.HARBOR_PROJECT, base_url=confHarbor.HARBOR_URL)

    harbor.users.create(username, password, email, realname, comment)
    return_model['retCode'] = 200
    return_model['retDesc'] = 'fail'
    return_model['data'] = None
    return jsonify(return_model)


@harbors.route('/list')
def get_image_list():
    """查詢鏡像倉庫的鏡像列表"""
    project = request.args.get('project', default=1)
    harbor = rest.get_harbor_client(api_version=None, username=confHarbor.HARBOR_USERNAME,password=confHarbor.HARBOR_PASSWORD,
                                    project=confHarbor.HARBOR_PROJECT, base_url=confHarbor.HARBOR_URL)
    repositories = harbor.repositories.list(project)
    return_model = {}
    data = []
    for repo in repositories:
        tags = harbor.repositories.list_tags(repo['name'])
        for tag in tags:
            item = repo.copy()
            manifest = harbor.repositories.get_manifests(item['name'],
                                                     tag['name'])
            size = 0

            for layer in manifest['manifest']['layers']:
                size += layer['size']
            item['size'] = str(size/(1024*1024)) + 'Mi'

            if tag['name'] != 'latest':
                item['name'] = repo['name'] + ":" + tag['name']
            data.append(item)

    return_model['retCode'] = 200
    return_model['retDesc'] = 'success'
    return_model['data'] = data

    fields = [
        "name", 'project_id', 'size',
        "tags_count", "star_count", "pull_count",
        "update_time"
    ]
    utils.print_list(data, fields)

    return jsonify(return_model)


if __name__ == "__main__":
    get_image_list()
