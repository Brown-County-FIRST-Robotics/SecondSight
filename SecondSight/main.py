#!/usr/bin/env python
import logging
import os.path
import sys
import time

import SecondSight.webserver.DEATHSTARE
import SecondSight.webserver.Server
import SecondSight.webserver.Config
import SecondSight.config
import SecondSight.Cameras
from flask import Flask
import threading
import SecondSight.AprilTags.Detector
import asyncio
import sys
import argparse
import networktables
import json


def mainLoop(app, tb):
    lastframetime = 0
    while True:
        newtime = time.time()
        towait = .1 - (newtime - lastframetime)
        if towait > 0:
            time.sleep(towait)
        lastframetime = newtime
        for cam in app.cameras:
            cam.update()
        app.apriltags = SecondSight.AprilTags.Detector.fetchApriltags(app.cameras)
        nt_send = []
        for det in app.apriltags:
            nt_send += [det['distance'], det['left_right'], det['up_down'], det['pitch'], det['roll'], det['yaw'],
                        det['distance_std'], det['left_right_std'], det['yaw_std'], det['rms'], det['error'],
                        det['tagid'], det['camera']]
        tb.putNumberArray('relative_positions', nt_send)


def main_cli():
    file_handler = logging.FileHandler(filename='logfile')
    stderr_handler = logging.StreamHandler(stream=sys.stderr)
    logging.basicConfig(level=getattr(logging, 'WARNING'), handlers=[file_handler, stderr_handler])

    config = SecondSight.config.loadConfig()
    networktables.NetworkTables.initialize(server=config.get_value('nt_dest'))
    april_table = networktables.NetworkTables.getTable('SecondSight').getSubTable('Apriltags')
    cameras = SecondSight.Cameras.loadCameras(config)
    app = SecondSight.webserver.Server.startFlask(cameras)
    while not config.get_value('cameras'):
        logging.critical('Waiting for cameras to be added to config, go to http://localhost:5000/config')
    while config.get_value('config_required'):
        time.sleep(0.001)
    mainLoop(app, april_table)


if __name__ == "__main__":
    # This file should never be run
    pass
