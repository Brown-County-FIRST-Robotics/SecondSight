#!/usr/bin/env python
import logging
import os.path
import subprocess
import sys
import time
import SecondSight
import threading
import asyncio
import sys
import git
import ntcore


def compress():
    for fname in os.listdir('logs'):
        if not fname.endswith('.gz'):
            threading.Thread(target=subprocess.call, args=(['gzip', f'logs/{fname}'],)).start()
    for fname in os.listdir('recordings'):
        print(fname)
        if fname.endswith('.avi'):
            def cmpr(filename):
                subprocess.call(['ffmpeg', '-i', f'recordings/{filename}', '-c:v', 'vp9', '-b:v', '500K', f'recordings/{filename.replace(".avi",".mp4")}'])
                os.remove(f'recordings/{filename}')
            threading.Thread(target=cmpr, args=(fname,)).start()


def main_cli():
    """
    This function acts like the main function in a normal program.
    Do the setup here then jump somewhere else
    """

    # Setup logging
    # TODO: use environment variables for these options eventually
    if not os.path.exists('logs/'):
        os.mkdir('logs')
    if not os.path.exists('recordings/'):
        os.mkdir('recordings')
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
    inst.startClient4(config.get_value('inst_name', 'SS_INST'))
    inst.setServer(config.get_value('nt_dest', 'localhost'))
    ping_start_time = time.time()
    while not inst.isConnected():
        time.sleep(0.01)
        if ping_start_time + 5 < time.time():
            break
    else:
        logging.critical("Failed to connect to networktables")
    table = inst.getTable(config.get_value('inst_name', 'SS_INST'))
    table.putString('config', config.stringify())
    repo = git.Repo('.')
    git_hash = repo.active_branch.commit.hexsha
    git_branch_name = repo.active_branch.name
    logging.info(f"Commit Hash:{git_hash}")
    logging.info(f"Branch Name:{git_branch_name}")
    table.putString("Hash", git_hash)
    table.putString("Branch", git_branch_name)
    if len(config.variables) == 0:
        table.putString("Error", "No_Config")

    # We run the Flask server here. We run it via threading, this is possibly wrong
    app = SecondSight.webserver.Server.startFlask()

    # Loop this forever, it's the main work loop
    # TODO: Any functionality specific to a module belongs in that module
    apriltag_manager = SecondSight.AprilTags.Manager.ApriltagManager.getInst()
    cams = SecondSight.Cameras.CameraManager.getCameras()
    if config.get_value('record_by_default', False):
        SecondSight.Recorder.RecordingManager.getInst().startRecording()
    try:
        while True:
            # Prevents loop overrun if no camera is in use
            if len(SecondSight.Cameras.CameraManager.getCameras())==0:
                time.sleep(0.1)
            # Update the cameras
            SecondSight.Cameras.CameraManager.updateAll()
            SecondSight.Recorder.RecordingManager.getInst().loop()

            # Acquire the AprilTag data
            apriltag_manager.fetchApriltags()
    except Exception as e:
        SecondSight.Recorder.RecordingManager.getInst().stopRecording()
        raise e


if __name__ == "__main__":
    # This file should never be run
    pass
