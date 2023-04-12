#!/usr/bin/env python

import sys
import time

import SecondSight.webserver.DEATHSTARE
import SecondSight.webserver.ApriltagAPI
import SecondSight.config
import SecondSight.Cameras
from flask import Flask
import threading
import SecondSight.AprilTags.Detector
import asyncio
import sys
import argparse


def fetchApriltags(cams):
    res = []
    for i, cam in enumerate(cams):  # TODO: Add thread pool
        if cam.role not in ['apriltag', '*']:
            continue

        dets = SecondSight.AprilTags.Detector.getPosition(cam.gray, cam.camera_matrix, None, roll_threshold=10000)
        if dets != []:
            for det in dets:
                det = det.json(error=True)
                det['camera'] = i
                res.append(det)
    return res


def main_cli():
    config = SecondSight.config.Configuration()
    config.set_path('config.json')
    cameras=[]
    for cam_config in config.get_value('cameras'):
        cameras.append(SecondSight.Cameras.Camera(cam_config['port'], cam_config['calibration'], cam_config['pos'], cam_config['role']))
    app = Flask(__name__)
    app.cameras = cameras
    app.apriltags = []
    SecondSight.webserver.DEATHSTARE.start(app)
    SecondSight.webserver.ApriltagAPI.start(app)
    threading.Thread(target=app.run, kwargs={'host': "0.0.0.0"}).start()
    lastframetime = 0
    while True:
        newtime = time.time()
        towait = .1 - (newtime - lastframetime)
        if towait > 0:
            time.sleep(towait)
        lastframetime = newtime
        for cam in cameras:
            cam.update()
        app.apriltags = fetchApriltags(cameras)


if __name__ == "__main__":
    # This file should never be run
    pass
