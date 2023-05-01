#!/usr/bin/env python

from typing import Union
from fastapi import FastAPI, Response
import logging

import SecondSight.Color
import SecondSight.Cameras
import SecondSight.config

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

if __name__ == "__main__":
    # This file should never be run
    pass
