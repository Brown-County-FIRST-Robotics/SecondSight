#!/usr/bin/env python

import logging
from flask import Flask, render_template, Response, redirect, request, jsonify
import SecondSight.Color


def start(app):
    @app.route('/')
    def index():
        """The default page"""
        return render_template('index.html')

    @app.route('/preview_image')
    def preview_image():
        logging.debug("DEATHSTARE.preview_image")
        the_camera = app.cameras[0]
        #Video streaming route. Put this in the src attribute of an img tag
        return Response(SecondSight.Color.gen_preview_picker(the_camera), mimetype='multipart/x-mixed-replace; boundary=frame')



if __name__ == "__main__":
    # This file should never be run
    pass
