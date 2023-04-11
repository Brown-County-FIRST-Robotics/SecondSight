#!/usr/bin/env python

import sys
import time

import SecondSight.webserver.DEATHSTARE
from flask import Flask
import threading
import asyncio

def main_cli():
    app = Flask(__name__)
    SecondSight.webserver.DEATHSTARE.start(app)
    threading.Thread(target=app.run,kwargs={'host': "0.0.0.0"}).start()
    while True:
        time.sleep(0.001)

if __name__ == "__main__":
    # This file should never be run
    pass
