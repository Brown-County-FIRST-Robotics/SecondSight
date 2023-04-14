#!/usr/bin/env python

import logging
from flask import Flask, render_template, Response, redirect, request, jsonify


def start(app):
    def gen_frames(camera, uncalibrated=False):  # generate frame by frame from camera
        logging.debug("DEATHSTARE.gen_frames")
        # We want to loop this forever
        while True:
            frame = camera.get_bytes(uncalibrated=uncalibrated)
            # Return the image to the browser
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')  # concat frame one by one and show result

    @app.route('/camera_feed/<int:number>')
    def camera_feed(number):
        return Response(gen_frames(app.cameras[number]), mimetype='multipart/x-mixed-replace; boundary=frame')

    @app.route('/')
    def index():
        """The default page"""
        return render_template('index.html')


if __name__ == "__main__":
    # This file should never be run
    pass