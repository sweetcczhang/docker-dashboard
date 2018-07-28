#!/usr/local/miniconda2/bin/python
# _*_ coding:utf-8 _*_
"""
# 程序的主入口
# @Time   : 2018/7/18 22:55
# @Author : 张城城
"""
from flask import Flask, render_template, jsonify
from flask_sockets import Sockets
from kube.blue import pods
from kube.hostInfo import hosts
from kube.deployments import deploy
from harbor.rest.restapi import harbors
from utility.DockerTerminal import StreamThread, KubernetesClient
from utility.HostTerminal import HostStreamThread
import paramiko
from paramiko.ssh_exception import AuthenticationException, SSHException
import confHarbor

app = Flask(__name__)
sockets = Sockets(app)
app.register_blueprint(pods, url_prefix='/admin')
app.register_blueprint(hosts, url_prefix='/host')
app.register_blueprint(deploy, url_prefix='/deploy')
app.register_blueprint(harbors, url_prefix='/harbor')


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
    return jsonify(return_model)


@app.route('/docker')
def docker_terminal():
    return render_template('index.html')


@app.route('/hosts')
def host_terminal():
    return render_template('index1.html')


@sockets.route('/echo')
def docker_socket(ws):
    print "Web socket is start......"
    client = KubernetesClient()
    resp = client.get_pod_exec()
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
    print "Web socket is start......"
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        ssh.connect(hostname='10.108.211.13', port=22, username='root', password='root!@#456')
    except AuthenticationException:
        raise Exception("auth failed user:%s ,passwd:%s" %
                        ('root', ''))
    except SSHException:
        raise Exception("could not connect to host:%s:%s" %
                        ('root', ''))

    print 'host has been connected.......'
    chan = ssh.invoke_shell(term='xterm')
    host = HostStreamThread(ws=ws, resp=chan)
    host.start()
    print 'web socket has work...... '
    while not ws.closed:
        command = ws.receive()
        if command is not None:
            print("Running command... %s\n" % command)
            chan.send(command)


if __name__ == '__main__':
    from gevent import pywsgi
    from geventwebsocket.handler import WebSocketHandler
    server = pywsgi.WSGIServer(('', 5000), app, handler_class=WebSocketHandler)
    server.serve_forever()

