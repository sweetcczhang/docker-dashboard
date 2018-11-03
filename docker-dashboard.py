#!/usr/local/miniconda2/bin/python
# _*_ coding:utf-8 _*_
"""
# 程序的主入口
# @Time   : 2018/7/18 22:55
# @Author : 张城城
"""
from flask import Flask, render_template, jsonify, request
from flask_sockets import Sockets
from kube.rest.blue import pods
from kube.rest.hostInfo import hosts
from kube.rest.services import service_s
from kube.rest.deployments import deploy
from kube.rest.autoscalingInfo import autoscaling
from harbor.rest.restapi import harbors
from terminal.pod_client import KubernetesClient
from terminal.pod_stream_thread import StreamThread
from terminal.host_stream_thread import HostStreamThread
from terminal.host_client import HostClient
from logs.restful.logs_info import logs
from jenkins1.restBuild import jenkin
import confHarbor
import yaml

app = Flask(__name__)
sockets = Sockets(app)
app.register_blueprint(pods, url_prefix='/admin')
app.register_blueprint(hosts, url_prefix='/host')
app.register_blueprint(deploy, url_prefix='/deploy')
app.register_blueprint(harbors, url_prefix='/harbor')
app.register_blueprint(service_s, url_prefix='/service')
app.register_blueprint(logs, url_prefix='/log')
app.register_blueprint(autoscaling, url_prefix='/autoScale')
app.register_blueprint(jenkin, url_prefix='/jenkins1')


@app.route('/test1')
def test():
    confHarbor.HARBOR_PASSWORD = 'sweetcc'
    confHarbor.HARBOR_USERNAME = 'sweetz'
    confHarbor.HARBOR_URL = 'http://host'
    return_model = {}
    return_model['retCode'] = confHarbor.HARBOR_PASSWORD
    return_model['retDesc'] = confHarbor.HARBOR_USERNAME
    return jsonify(return_model)


@app.route('/test2', methods=['GET', 'POST'])
def test1():
    texts = request.values.get(key='yaml')
    print texts
    l=yaml.load(texts)
    print l
    return_model = {}
    return_model['retCode'] = confHarbor.HARBOR_PASSWORD
    return_model['retDesc'] = confHarbor.HARBOR_USERNAME
    print "sssss"
    return jsonify(return_model)


@app.route('/docker', methods=['GET', 'POST'])
def docker_terminal():
    return render_template('index.html')


@app.route('/hosts')
def host_terminal():
    return render_template('index1.html')


@sockets.route('/zcc')
def docker_socket(ws):
    """
    pod容器的web terminal
    :param ws:
    :return:
    """
    print "Web socket is start......"
    pod_name = request.args.get("name")
    client = KubernetesClient()
    resp = client.get_pod_exec(name=pod_name)
    print 'pod has been created.......'
    thread_stream = StreamThread(ws=ws, resp=resp)
    thread_stream.start()
    while not ws.closed:
        command = ws.receive()
        if command is not None:
            print("Running command... %s\n" % command)
            resp.write_stdin(command)


@sockets.route('/echo1')
def connect_host(ws):
    """
    主机的web terminal
    :param ws:
    :return:
    """
    print request.values.get('host')
    hostname = request.values.get('host', '10.108.210.194')
    print "hello"
    host_client = HostClient()
    print "world"
    chan = host_client.get_invoke_shell(hostname=hostname)
    host = HostStreamThread(ws=ws, resp=chan)
    host.start()
    print 'web socket has work......'
    while not ws.closed:
        command = ws.receive()
        if command is not None:
            print("Running command... %s\n" % command)
            chan.send(command)


if __name__ == '__main__':
    from gevent import pywsgi
    from geventwebsocket.handler import WebSocketHandler
    server = pywsgi.WSGIServer(('', 5001), app, handler_class=WebSocketHandler)
    server.serve_forever()


