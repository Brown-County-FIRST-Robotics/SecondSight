#!/usr/bin/env python
import logging
import os.path
import sys
import time
import SecondSight
import threading
import asyncio
import sys
import networktables


def mainLoop():
    """
    Main loop for the program. Once setup is complete, this loops forever
    """

    config = SecondSight.config.Configuration()

    # We can put data on NetworkTables
    # TODO: Only do this if the configuration says to do it
    # TODO: Every module should write to network tables, not from here
    networktables.NetworkTables.initialize(server=config.get_value('nt_dest'))
    april_table = networktables.NetworkTables.getTable('SecondSight').getSubTable('Apriltags')
    conecube_table = networktables.NetworkTables.getTable('SecondSight').getSubTable('GamePieces')

    # We run the Flask server here. We run it via threading, this is possibly wrong
    app = SecondSight.webserver.Server.startFlask()

    # Loop this forever, it's the main work loop
    # TODO: Any functionality specific to a module belongs in that module
    lastframetime = 0
    while True:
        
        # Only run the loop every 100ms
        newtime = time.time()
        towait = .1 - (newtime - lastframetime)
        if towait > 0:
            time.sleep(towait)
        lastframetime = newtime

        # Update the cameras
        for cam in app.cameras:
            cam.update()
        
        # Acquire the AprilTag data
        # TODO: Most of this belongs in the AprilTag module
        if "apriltags" in [i[:min(len(i)-1,9)] for i in config.get_value('detects')]:
            app.apriltags = SecondSight.AprilTags.Detector.fetchApriltags(app.cameras)
            nt_send = []
            for det in app.apriltags:
                nt_send += [det['distance'], det['left_right'], det['up_down'], det['pitch'], det['roll'], det['yaw'],
                            det['distance_std'], det['left_right_std'], det['yaw_std'], det['rms'], det['error'],
                            det['tagid'], det['camera']]
            april_table.putNumberArray('relative_positions', nt_send)
        app.game_pieces = SecondSight.Color.postGamePieces(conecube_table, app.cameras, config.get_value('detects'))


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

    mainLoop()


if __name__ == "__main__":
    # This file should never be run
    pass
