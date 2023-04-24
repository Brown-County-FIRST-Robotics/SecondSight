#!/usr/bin/env python

import logging
from flask import Flask, render_template, Response, redirect, request, jsonify

app = Flask(__name__)

@app.route('/')
def index():
    """The default page"""
    return render_template('index.html')

if __name__ == "__main__":
    # This file should never be run
    pass
