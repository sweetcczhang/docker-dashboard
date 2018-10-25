#!/usr/local/miniconda2/bin/python
# _*_ coding:utf-8 _*_
"""
# @Project : docker-dashboard
# @Time    : 2018/10/25 下午3:45
# @Author  : zhangchengcheng
# @FileName: pod_client.py
# @Github  : https://github.com/sweetcczhang
"""

import time
from kubernetes import config
from kubernetes.client import Configuration
from kubernetes.client.apis import core_v1_api
from kubernetes.client.rest import ApiException
from kubernetes.stream import stream


class KubernetesClient(object):
    def __init__(self):
        config.load_kube_config(config_file='/root/zcc/hello/config')
        c = Configuration()
        c.assert_hostname = False
        Configuration.set_default(c)
        self.api = core_v1_api.CoreV1Api()

    def get_pod_exec(self):
        api = self.api
        name = 'busybox-test1'
        resp = None
        try:
            resp = api.read_namespaced_pod(name=name, namespace='default')
        except ApiException as e:
            if e.status != 404:
                print ("Unknown error: %s" %e)
                exit(1)

            if not resp:
                print("Pod %s does not exits. Creating it..." % name)
                pod_manifest = {
                    'apiVersion': 'v1',
                    'kind': 'Pod',
                    'metadata': {
                        'name': name
                    },
                    'spec': {
                        'containers': [{
                            'image': 'busybox',
                            'name': 'sleep',
                            "args": [
                                "/bin/sh",
                                "-c",
                                "while true;do date;sleep 5; done"
                            ]
                        }]
                    }
                }
                api.create_namespaced_pod(body=pod_manifest, namespace='default')
                while True:
                    resp = api.read_namespaced_pod(name=name,
                                                   namespace='default')
                    if resp.status.phase != 'Pending':
                        break
                    time.sleep(1)
                print("Done.")

        # calling exec and wait for response.

        exec_command = [
            "/bin/sh",
            "-c",
            'TERM=xterm-256color; export TERM; [ -x /bin/bash ] && ([ -x /usr/bin/script ] && '
            '/usr/bin/script -q -c "/bin/bash" /dev/null || exec /bin/bash) || exec /bin/sh']

        # Calling exec interactively.
        resp = stream(api.connect_get_namespaced_pod_exec, name, 'default',
                      command=exec_command,
                      stderr=True, stdin=True,
                      stdout=True, tty=True,
                      _preload_content=False)
        return resp
