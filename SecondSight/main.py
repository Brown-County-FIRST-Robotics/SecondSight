#!/usr/bin/env python

import sys
import time

import SecondSight.webserver.DEATHSTARE
import SecondSight.config
import SecondSight.Cameras
from flask import Flask
import threading
import SecondSight.AprilTags
import asyncio
import sys
import argparse

def main_cli():
    config = SecondSight.config.Configuration()
    config.set_path('config.json')
    cameras=[]
    for cam_config in config.get_value('cameras'):
        cameras.append(SecondSight.Cameras.Camera(cam_config['port'], cam_config['calibration'], cam_config['pos'], cam_config['role']))
    app = Flask(__name__)
    app.cameras=cameras
    SecondSight.webserver.DEATHSTARE.start(app)
    threading.Thread(target=app.run,kwargs={'host': "0.0.0.0"}).start()
    lastframetime = 0
    while True:
        newtime = time.time()
        towait = .1 - (newtime - lastframetime)
        if towait > 0:
            time.sleep(towait)
        lastframetime = newtime
        for cam in cameras:
            cam.update()

if __name__ == "__main__":
    # This file should never be run
    pass
