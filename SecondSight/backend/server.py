#!/usr/bin/env python

from typing import Union
from fastapi import FastAPI, Response
import logging

import SecondSight.Color
import SecondSight.Cameras
import SecondSight.config


config = SecondSight.config.Configuration()
config.set_path("config.json")

# Do this to open the cameras before we need them
cameras = SecondSight.Cameras.loadCameras()
cameras[0].update()

app = FastAPI()

@app.get("/")
def read_root():
    # return some details on what the app is
    return {"application": "SecondSight"}


if __name__ == "__main__":
    # This file should never be run
    pass
