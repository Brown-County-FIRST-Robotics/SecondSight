#!/usr/bin/env python

from typing import Union, List
from fastapi import FastAPI, Response
from fastapi.responses import StreamingResponse
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles

import logging
import time

import SecondSight.Color
import SecondSight.Cameras
import SecondSight.config
from fastapi.middleware.cors import CORSMiddleware

def gen_frames(camera):  # generate frame by frame from camera
    """
    Generator to return camera frames at a set framerate
    """
    logging.debug("backend.gen_frames")
    
    last_frame_time = 0
    framerate = 10 # Get this from the config file eventually

    while True:
        while time.time() - last_frame_time < 1 / framerate:
            time.sleep(0.001)
        frame = camera.get_bytes()
        # Return the image to the browser
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')  # concat frame one by one and show result
        last_frame_time = time.time()

app = FastAPI()

#    "http://localhost:5000",
origins = [
    "*",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



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

@app.get("/get_cameras")
def get_cameras() -> List[str]:
    cameras = SecondSight.Cameras.CameraManager.getCameras()

    # We return a list of integers, each integer represents a camera
    return list(range(0, len(cameras)))

@app.get("/camera/{camera_id}")
def get_camera(camera_id) -> StreamingResponse:

    camera = SecondSight.Cameras.CameraManager.getCamera(int(camera_id))
    return StreamingResponse(gen_frames(camera), media_type="multipart/x-mixed-replace;boundary=frame")

# This code needs a few changes
@app.get('/preview_image')
def preview_image():
    logging.debug("backend.preview_image")
    the_camera = SecondSight.Cameras.CameraManager.getCamera(0)
    # Video streaming route. Put this in the src attribute of an img tag
    return StreamingResponse(SecondSight.Color.gen_preview_picker(the_camera), media_type='multipart/x-mixed-replace; boundary=frame')

app.mount("/frontend", StaticFiles(directory="/home/bress/src/SecondSight-josh/SecondSight/frontend/static/build/"), name="frontend")

if __name__ == "__main__":
    # This file should never be run
    pass
