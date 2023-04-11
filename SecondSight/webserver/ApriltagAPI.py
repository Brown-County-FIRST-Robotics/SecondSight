#!/usr/bin/env python

import logging
from flask import Flask, render_template, Response, redirect, request, jsonify
import SecondSight.AprilTags.Detector


def start(app):
    @app.route('/apriltag/pixel_coords')
    def pixel_coords():
        res=[]
        for i,cam in enumerate(app.cameras):# TODO: Add thread pool
            dets=SecondSight.AprilTags.Detector.getCoords(cam.gray)
            if dets!=[]:
                for det in dets:
                    print(det)
                    res.append({"coords":det[0], "tagid":det[1], "camera":i})
        return jsonify(res)




if __name__ == "__main__":
    # This file should never be run
    pass