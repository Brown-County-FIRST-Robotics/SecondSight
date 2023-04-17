#!/usr/bin/env python

import logging
from flask import Flask, render_template, Response, redirect, request, jsonify
import SecondSight


def start(app):
    @app.route('/game_pieces/cone_2023')
    def cone_2023():
        return jsonify(app.game_pieces['cone2023'])


if __name__ == "__main__":
    # This file should never be run
    pass
