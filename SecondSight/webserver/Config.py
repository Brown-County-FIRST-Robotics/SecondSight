#!/usr/bin/env python

import logging
from flask import Flask, render_template, Response, redirect, request, jsonify
import SecondSight.config



def start(app):
    @app.route('/config', methods=['GET', 'POST'])
    def config():
        if request.method=='GET':
            return render_template('config.html')
        else:
            print(list(request.form.items()))
            conf=SecondSight.config.Configuration()  # I think this is how singleton classes work
            conf.set_value('nt_dest', request.form['nt_addr'])
            conf.set_value('cameras', [])
            for k,v in request.form.items():
                if k[:9]=='cam_port_':
                    conf.variables['cameras'].append(
                        {
                            'port': v,
                            'calibration': None,
                            'role': 'conecube',
                            'pos': None
                         })
            conf.write()
            return redirect('/')
if __name__ == "__main__":
    # This file should never be run
    pass