import logging
import threading

import flask_socketio
import socketio
from flask import Flask, render_template, Response, redirect, request, jsonify
from markupsafe import Markup

import SecondSight
import time


def start(app:Flask, socketsz:flask_socketio.SocketIO):
    @app.route('/')
    def index():
        return render_template('index.html')
    @app.route('/camera/<int:id>')
    def camera(id:int):
        return render_template('camera.html', ind=id)
    @socketsz.on('connect', '/camera/0')
    def handle_connect():
        print('perasona colbnn')
        socketsz.emit('update_camera_properties',[{"path":"patth","failing":False,"calibrated":True, "name":"camera mccamera face"},
                                                 {"path":"patth2","failing":True,"calibrated":True, "name":"FR2"},
                                                 {"path":"patth3","failing":False,"calibrated":False, "name":"FL3"},
                                                 {"path":"patth4","failing":False,"calibrated":False, "name":"FL43"}])

    @socketsz.on('resasdsadasend_data', '/camera/0')
    def handle_connecdasdt(da):
        print('hiiii')
        socketsz.emit('update_camera_properties', [{"path": "patth", "failing": False, "calibrated": True, "name": "camera mccamera face"},
                                                  {"path": "patth2", "failing": True, "calibrated": True, "name": "FR2"},
                                                  {"path": "patth3", "failing": False, "calibrated": False, "name": "FL3"},
                                                  {"path": "patth4", "failing": False, "calibrated": False, "name": "FL43"}],to='all')

    def k():
        while True:
            socketsz.emit('update_camera_properties', [{"path": "patth", "failing": False, "calibrated": True, "name": "camera mccamera face"},
                                                  {"path": "patth2", "failing": True, "calibrated": True, "name": "FR2"},
                                                  {"path": "patth3", "failing": False, "calibrated": False, "name": "FL3"},
                                                  {"path": "patth4", "failing": False, "calibrated": False, "name": "FL43"}],to='all')
            time.sleep(1)
    threading.Thread(target=k).start()

