#!/usr/bin/env python

import logging
from flask import Flask, render_template, Response, redirect, request, jsonify
import SecondSight.AprilTags.Detector


def start(app):
    @app.route('/apriltag/april_coords') # TODO: add query parameter for error
    def april_coords():
        print(app.apriltags)
        return jsonify(app.apriltags)




if __name__ == "__main__":
    # This file should never be run
    pass