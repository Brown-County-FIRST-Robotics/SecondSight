#!/usr/bin/env python

from typing import Union
from fastapi import FastAPI, Response
from fastapi.responses import StreamingResponse
import logging
import time

import SecondSight.Color
import SecondSight.Cameras
import SecondSight.config


def gen_frames(camera):  # generate frame by frame from camera
    """
    Generator to return camera frames at a set framerate
    """
    logging.debug("backend.gen_frames")
    
    last_frame_time = 0
    framerate = 10 # Get this from the config file

    while True:
        while time.time() - last_frame_time < 1 / framerate:
            time.sleep(0.001)
        frame = camera.get_bytes()
        # Return the image to the browser
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')  # concat frame one by one and show result
        last_frame_time = time.time()

app = FastAPI()

@app.get("/")
def read_root():
    # return some details on what the app is
    return {"application": "SecondSight"}

@app.get("/config")
def read_config():
    #Return the configuration details

    c = SecondSight.config.Configuration()

    return c.get_all()

@app.post("/config")
def set_config(config_values: dict):
    # Sets a configuration variable

    c = SecondSight.config.Configuration()

    for k in config_values.keys():
        c.set_value(k, config_values[k])

    c.write()

@app.get("/config/{config_id}")
def get_config(config_id):

    c = SecondSight.config.Configuration()
    return c.get_value(config_id)

@app.get("/camera/{camera_id}")
def get_camera(camera_id) -> StreamingResponse:

    c = SecondSight.config.Configuration()
    camera = SecondSight.Cameras.getCamera(int(camera_id))

    return StreamingResponse(gen_frames(camera), media_type="multipart/x-mixed-replace;boundary=frame")

if __name__ == "__main__":
    # This file should never be run
    pass
