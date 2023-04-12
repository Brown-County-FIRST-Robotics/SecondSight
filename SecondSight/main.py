#!/usr/bin/env python
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


def mainLoop(app):
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


def main_cli():
    config=SecondSight.config.loadConfig()
    cameras=SecondSight.Cameras.loadCameras(config)
    app=SecondSight.webserver.Server.startFlask(cameras)
    while not config.get_value('cameras'):
        print('Waiting for cameras to be added to config')
    mainLoop(app)


if __name__ == "__main__":
    # This file should never be run
    pass
