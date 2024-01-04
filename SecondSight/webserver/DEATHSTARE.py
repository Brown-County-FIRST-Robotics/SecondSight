#!/usr/bin/env python

import logging
from flask import Flask, render_template, Response, redirect, request, jsonify
from markupsafe import Markup

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
        cams=''
        for i, cam in enumerate(config.get_value('cameras')):
            cam=SecondSight.Cameras.CameraManager.getCamera(i)
            cams += f'''
            <div class="camera">
                <h2{' class="error"' if cam.failing else ''}>Camera {i+1}{' (Failing!)' if cam.failing else ''}</h2>
                <a href="/camera_feed/{i}">Feed</a>
                <p>Port: {cam.device}</p>
                <p>{'Roles:'+', '.join(cam.roles) if len(cam.roles)>0 else 'No roles assigned'}</p>
                <p{' class="error">Not c' if cam.map2 is None else '>C'}alibrated</p>
                <a href="/calibration?camera={i}">Calibrate</a>
            </div>
            '''
        
        """The default page"""
        return render_template('index.html', cams=Markup(cams))

    # This code needs a few changes
    @app.route('/preview_image')
    def preview_image():
        logging.debug("DEATHSTARE.preview_image")
        the_camera = SecondSight.Cameras.CameraManager.getCamera(0)
        # Video streaming route. Put this in the src attribute of an img tag
        return Response(SecondSight.Color.gen_preview_picker(the_camera), mimetype='multipart/x-mixed-replace; boundary=frame')

    @app.route('/calibration')
    def calibration():
        args = request.args.to_dict()
        logging.debug("DEATHSTARE.calibration")
        if 'camera' not in args:
            args['camera'] = '0'
        if 'min_captures' not in args:
            args['min_captures'] = '30'
        # Video streaming route. Put this in the src attribute of an img tag
        return Response(SecondSight.Calibration.genCalibrationFrames(int(args['camera']), min_captures=int(args['min_captures'])), mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == "__main__":
    # This file should never be run
    pass
