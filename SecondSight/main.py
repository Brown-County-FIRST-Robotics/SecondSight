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


def mainLoop():

    config = SecondSight.config.Configuration()
    networktables.NetworkTables.initialize(server=config.get_value('nt_dest'))
    april_table = networktables.NetworkTables.getTable('SecondSight').getSubTable('Apriltags')

    app = SecondSight.webserver.Server.startFlask()
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
        april_table.putNumberArray('relative_positions', nt_send)


def main_cli():
    file_handler = logging.FileHandler(filename='logfile')
    stderr_handler = logging.StreamHandler(stream=sys.stderr)
    config = SecondSight.config.Configuration()
    config.set_path("config.json")
    logging.basicConfig(level=getattr(logging, 'WARNING'), handlers=[file_handler, stderr_handler])

    mainLoop()


if __name__ == "__main__":
    # This file should never be run
    pass
