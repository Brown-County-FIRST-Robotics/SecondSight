#!/usr/bin/env python

import logging
import requests
import SecondSight.config
from flask import Flask, render_template, Response, redirect, request, jsonify, send_from_directory
from flask_cors import CORS #comment this on deployment

app = Flask(__name__, static_url_path='', static_folder='static/build')
CORS(app, resources={r"*": {"origins": ["http:localhost:8000"]}})

@app.route("/", defaults={'path':''})
def serve(path):
    return send_from_directory(app.static_folder,'index.html')

if __name__ == "__main__":
    # This file should never be run
    pass
