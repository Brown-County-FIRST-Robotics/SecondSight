import logging

import flask_socketio
from flask import Flask, render_template, Response, redirect, request, jsonify
from markupsafe import Markup

import SecondSight
import time


def start(app:Flask, sockets:flask_socketio.SocketIO):
    @app.route('/')
    def index():
        return render_template('index.html')

    @sockets.on('connect')
    def handle_connect():
        sockets.emit('update_camera_properties',[{"path":"patth","failing":False,"calibrated":True, "name":"camera mccamera face"},
                                                 {"path":"patth2","failing":True,"calibrated":True, "name":"FR2"},
                                                 {"path":"patth3","failing":False,"calibrated":False, "name":"FL3"},
                                                 {"path":"patth4","failing":False,"calibrated":False, "name":"FL43"}])
