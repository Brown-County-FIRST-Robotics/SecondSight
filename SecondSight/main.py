#!/usr/bin/env python
import logging
import os.path
import sys
import time
import SecondSight
import threading
import asyncio
import sys
import ntcore

def main_cli():
    """
    This function acts like the main function in a normal program.
    Do the setup here then jump somewhere else
    """

    # Setup logging
    # TODO: use environment variables for these options eventually
    file_handler = logging.FileHandler(filename='logfile')
    stderr_handler = logging.StreamHandler(stream=sys.stderr)
    logging.basicConfig(level=getattr(logging, 'WARNING'), handlers=[file_handler, stderr_handler])

    # Load the config file and set the path
    # TODO: Put this config file in a home directory someday
    config = SecondSight.config.Configuration()
    config.set_path("config.json")
    SecondSight.Cameras.CameraManager.loadCameras()

    # We can put data on NetworkTables
    # TODO: Only do this if the configuration says to do it
    # TODO: Every module should write to network tables, not from here
    inst=ntcore.NetworkTableInstance.getDefault()
    inst.setServer(config.get_value('nt_dest'))

    # We run the Flask server here. We run it via threading, this is possibly wrong
    app = SecondSight.webserver.Server.startFlask()

    # Loop this forever, it's the main work loop
    # TODO: Any functionality specific to a module belongs in that module
    lastframetime = 0
    apriltag_manager = SecondSight.AprilTags.Manager.ApriltagManager.getInst()
    cams = SecondSight.Cameras.CameraManager.getCameras()
    while True:
        # Only run the loop every 100ms
        newtime = time.time()
        towait = .1 - (newtime - lastframetime)
        if towait > 0:
            time.sleep(towait)
        lastframetime = newtime

        # Update the cameras
        SecondSight.Cameras.CameraManager.updateAll()

        # Acquire the AprilTag data
        apriltag_manager.fetchApriltags()


if __name__ == "__main__":
    # This file should never be run
    pass
