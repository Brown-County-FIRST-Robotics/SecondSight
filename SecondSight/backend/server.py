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


if __name__ == "__main__":
    # This file should never be run
    pass
