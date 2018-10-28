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
from kube.rest.services import sevices
from kube.rest.deployments import deploy
from harbor.rest.restapi import harbors
from terminal.pod_client import KubernetesClient
from terminal.pod_stream_thread import StreamThread
from terminal.host_stream_thread import HostStreamThread
from terminal.host_client import HostClient
from logs.restful.logs_info import logs
import confHarbor

app = Flask(__name__)
sockets = Sockets(app)
app.register_blueprint(pods, url_prefix='/admin')
app.register_blueprint(hosts, url_prefix='/host')
app.register_blueprint(deploy, url_prefix='/deploy')
app.register_blueprint(harbors, url_prefix='/harbor')
app.register_blueprint(sevices, url_prefix='/service')
app.register_blueprint(logs, url_prefix='/log')

@app.route('/test1')
def test():
    confHarbor.HARBOR_PASSWORD = 'sweetcc'
    confHarbor.HARBOR_USERNAME = 'sweetz'
    confHarbor.HARBOR_URL = 'http://host'
    return_model = {}
    return_model['retCode'] = confHarbor.HARBOR_PASSWORD
    return_model['retDesc'] = confHarbor.HARBOR_USERNAME
    return jsonify(return_model)


@app.route('/test2')
def test1():
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
    print request.args.get('host')
    hostname = request.args.get('host', '10.108.210.194')
    host_client = HostClient()
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


