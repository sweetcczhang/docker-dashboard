#!/usr/bin/env python
# coding: utf-8
"""
# @Time   : 2018/7/14 17:27
# @Author : 张城城
"""
import time
from kubernetes import config
from kubernetes.client import Configuration
from kubernetes.client.apis import core_v1_api
from kubernetes.client.rest import ApiException
from kubernetes.stream import stream
import threading


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


class StreamThread(threading.Thread):

    def __init__(self, ws, resp):
        super(StreamThread, self).__init__()
        self.ws = ws
        self.resp = resp

    def run(self):
        # return resp
        while (not self.ws.closed) and (self.resp.is_open()):
            try:
                self.resp.update(timeout=1)
                if self.resp.peek_stdout():
                    message = self.resp.read_stdout()
                    self.ws.send(str(message))
                    print("STDOUT: %s" % message)
                if self.resp.peek_stderr():
                    message = self.resp.read_stderr()
                    self.ws.send(str(message))
                    print("STDERR: %s" % message)
            except Exception as e:
                print("docker daemon socket err: %s" % e)
                self.ws.close()
                self.resp.close()
                break

