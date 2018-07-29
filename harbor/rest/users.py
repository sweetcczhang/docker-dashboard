#!/usr/local/miniconda2/bin/python
# _*_ coding:utf-8 _*_
"""
# @Time   : 2018/7/28 21:20
# @Author : 张城城
"""

from flask import request, jsonify
from harbor.rest import harbor as harbor_client
from harbor.rest.restapi import harbors
import confHarbor
from harbor import exceptions as exp
from harbor import utils


@harbors.route('/deleteUser', methods={'POST', 'GET'})
def delete_user():
    username = request.args.get('username', None)
    return_model = {}

    if harbor_client.users.is_id(username):
        id = username
    else:
        id = harbor_client.users.get_id_by_name(username)
    harbor_client.users.delete(id)
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

    harbor_client.users.create(username, password, email, realname, comment)
    return_model['retCode'] = 200
    return_model['retDesc'] = 'fail'
    return_model['data'] = None
    return jsonify(return_model)


def do_user_list(cs, args):
    """Get registered users of Harbor."""
    try:
        users = harbor_client.users.list()
    except exp.Forbidden as e:
        raise exp.CommandError(e.message)
    # Get admin user
    try:
        admin = harbor_client.users.get(1)
        users.append(admin)
    except Exception:
        pass
    fields = ['user_id', 'username', 'is_admin',
              'email', 'realname', 'comment']
    formatters = {"is_admin": 'has_admin_role'}
    utils.print_list(users, fields, formatters=formatters, sortby=args.sortby)