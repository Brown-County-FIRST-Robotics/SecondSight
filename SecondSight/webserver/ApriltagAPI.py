#!/usr/bin/env python

import logging
from flask import Flask, render_template, Response, redirect, request, jsonify
import SecondSight


def start(app):
    @app.route('/apriltag/april_coords')
    def april_coords():
        return jsonify(app.apriltags)




if __name__ == "__main__":
    # This file should never be run
    pass