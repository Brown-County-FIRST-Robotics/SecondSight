#!/usr/bin/env python
import logging
import os.path
import sys
import time
import SecondSight
import threading
import asyncio
import sys
import git
import ntcore

def main_cli():
    """
    This function acts like the main function in a normal program.
    Do the setup here then jump somewhere else
    """

    # Setup logging
    # TODO: use environment variables for these options eventually
    file_handler = logging.FileHandler(filename=f'logs/{SecondSight.utils.get8601date()}')
    stderr_handler = logging.StreamHandler(stream=sys.stderr)
    logging.basicConfig(level=logging.DEBUG, handlers=[file_handler, stderr_handler])

    # Load the config file and set the path
    # TODO: Put this config file in a home directory someday
    config = SecondSight.config.Configuration()
    config.set_path("config.json")
    SecondSight.Cameras.CameraManager.loadCameras()

    # We can put data on NetworkTables
    # TODO: Only do this if the configuration says to do it
    # TODO: Every module should write to network tables, not from here
    inst = ntcore.NetworkTableInstance.getDefault()
    inst.startClient4(config.get_value('inst_name'))
    inst.setServer(config.get_value('nt_dest'))
    table = inst.getTable(config.get_value('inst_name'))
    table.putString('config', config.stringify())
    repo=git.Repo('.')
    git_hash=repo.active_branch.commit.hexsha
    git_branch_name=repo.active_branch.name
    logging.debug(f"Commit Hash:{git_hash}")
    logging.debug(f"Branch Name:{git_branch_name}")
    table.putString("Hash", git_hash)
    table.putString("Branch", git_branch_name)

    # We run the Flask server here. We run it via threading, this is possibly wrong
    app = SecondSight.webserver.Server.startFlask()

    # Loop this forever, it's the main work loop
    # TODO: Any functionality specific to a module belongs in that module
    apriltag_manager = SecondSight.AprilTags.Manager.ApriltagManager.getInst()
    cams = SecondSight.Cameras.CameraManager.getCameras()
    SecondSight.Recorder.RecordingManager.getInst().startRecording()
    try:
        while True:
            # Update the cameras
            SecondSight.Cameras.CameraManager.updateAll()
            SecondSight.Recorder.RecordingManager.getInst().loop()

            # Acquire the AprilTag data
            apriltag_manager.fetchApriltags()
    except Exception as _:
        SecondSight.Recorder.RecordingManager.getInst().stopRecording()


if __name__ == "__main__":
    # This file should never be run
    pass
