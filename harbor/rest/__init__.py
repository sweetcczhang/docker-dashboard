#!/usr/local/miniconda2/bin/python
# _*_ coding:utf-8 _*_
"""
# @Time   : 2018/7/22 16:42
# @Author : 张城城
"""
import harbor
from harbor import api_versions
from harbor import client
from harbor import exceptions as exc
from harbor import utils
import confHarbor

DEFAULT_API_VERSION = "2.0"
DEFAULT_MAJOR_OS_COMPUTE_API_VERSION = "2.0"


def get_harbor_client(api_version=None, username=None, password=None, project=None, base_url=None):
    if not api_version:
        api_version = api_versions.get_api_version(
            DEFAULT_MAJOR_OS_COMPUTE_API_VERSION)
    if not username:
        username = utils.env('HARBOR_USERNAME')
    if not password:
        password = utils.env('HARBOR_PASSWORD')
    if not project:
        project = utils.env('HARBOR_PROJECT')
    if not base_url:
        base_url = utils.env('HARBOR_URL')

    clients = client.Client(api_version, username, password, project, base_url)
    try:
        clients.authenticate()
    except exc.Unauthorized:
        raise exc.CommandError("Invalid Harbor credentials.")
    except exc.AuthorizationFailure as e:
        raise exc.CommandError("Unable to authorize user '%s': %s"
                               % (username, e))
    return clients

# harbor = get_harbor_client(api_version=None, username=confHarbor.HARBOR_USERNAME,
#                                     password=confHarbor.HARBOR_PASSWORD,
#                                     project=confHarbor.HARBOR_PROJECT, base_url=confHarbor.HARBOR_URL)
harbor = ''