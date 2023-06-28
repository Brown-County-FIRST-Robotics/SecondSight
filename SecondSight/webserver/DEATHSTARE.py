#!/usr/bin/env python

import logging
from flask import Flask, render_template, Response, redirect, request, jsonify
import SecondSight
import time


def start(app):
    def gen_frames(camera, uncalibrated=False, framerate=10):  # generate frame by frame from camera
        logging.debug("DEATHSTARE.gen_frames")
        # We want to loop this forever
        last_frame_time = 0
        while True:
            while time.time() - last_frame_time < 1 / framerate:
                time.sleep(0.001)
            frame = camera.get_bytes(uncalibrated=uncalibrated)
            # Return the image to the browser
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')  # concat frame one by one and show result
            last_frame_time = time.time()

    @app.route('/camera_feed/<int:number>')
    def camera_feed(number):
        args = request.args.to_dict()
        framerate = 10
        cam = SecondSight.Cameras.CameraManager.getCamera(number)
        if 'framerate' in args:
            framerate = float(args['framerate'])
        if 'uncalibrated' in args:
            return Response(
                gen_frames(cam, uncalibrated=(args['uncalibrated'] == 'true'), framerate=framerate),
                mimetype='multipart/x-mixed-replace; boundary=frame')
        return Response(gen_frames(cam, framerate=framerate),
                        mimetype='multipart/x-mixed-replace; boundary=frame')

    @app.route('/')
    def index():
        # if config is needed, redirect to create config screen
        config = SecondSight.config.Configuration() 
        if config.get_value('config_required'):
            return redirect('/config')
        
        """The default page"""
        return render_template('index.html')


if __name__ == "__main__":
    # This file should never be run
    pass
