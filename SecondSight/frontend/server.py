#!/usr/bin/env python

import logging
import requests
import SecondSight.config
from flask import Flask, render_template, Response, redirect, request, jsonify

app = Flask(__name__)

@app.route('/')
def index():
    """The default page"""

    config = SecondSight.config.Configuration()
    backend_url = config.get_value("backend_url")

    response = requests.get("%s/get_cameras" % backend_url)
    cams = response.json()
    return render_template('index.html', cams=cams, backend_url=backend_url)

if __name__ == "__main__":
    # This file should never be run
    pass
