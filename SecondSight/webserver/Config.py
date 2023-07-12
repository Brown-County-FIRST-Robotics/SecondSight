#!/usr/bin/env python

import logging
from flask import Flask, render_template, Response, redirect, request, jsonify, Markup
import SecondSight


def start(app):
    @app.route('/config', methods=['GET', 'POST'])
    def config():
        conf = SecondSight.config.Configuration()  # I think this is how singleton classes work
        if request.method == 'GET':
            cams = ''
            if conf.get_value('cameras') is None:
                conf.set_value('cameras', [])
            for i, cam in enumerate(conf.get_value('cameras')):
                cams += f'''
                <label for="cam_port_{i}">Camera port</label><br>
                <input type="text" id="cam_port_{i}" name="cam_port_{i}" value="{cam['port']}"><br>
                <label>
                        <input type="checkbox" name="game_objs_{i}" {'checked' if 'conecube' in cam['role'] else ''}>
                         game objects
                    </label><br>
                    <label>
                        <input type="checkbox" name="apriltags_{i}" {'checked' if 'apriltag' in cam['role'] else ''}>
                         apriltags
                </label><br>
                '''
            return render_template('config.html', nt_dest=conf.get_value('nt_dest'), cams=Markup(cams))
        else:
            conf.set_value('nt_dest', request.form['nt_addr'])
            conf.set_value('cameras', [])
            conf.set_value('detects', [])
            for k, v in request.form.items():
                if k == 'cube2023':
                    conf.set_value('detects', conf.get_value('detects')+['cube2023'])
                if k == 'apriltags2023':
                    assert not any([i.startswith('apriltags') for i in conf.get_value('detects')]), 'Only one year of apriltags are allowed'  # TODO: turn this into a web response
                    conf.set_value('detects', conf.get_value('detects')+['apriltags2023'])
                if k.startswith('cam_port_'):
                    roles = []
                    if f"apriltags_{k.split('_')[-1]}" in request.form:
                        if request.form[f"apriltags_{k.split('_')[-1]}"] == 'on':
                            roles.append('apriltags')
                    if f"game_objs_{k.split('_')[-1]}" in request.form:
                        if request.form[f"game_objs_{k.split('_')[-1]}"] == 'on':
                            roles.append('gamepieces')
                    conf.set_value('cameras', conf.get_value('cameras') +
                                   [{
                                       'port': v,
                                       'calibration': None,
                                       'role': roles,
                                       'pos': None
                                   }])
            SecondSight.Cameras.CameraManager.loadCameras()
            conf.set_value('config_required', False)
            conf.write()
            return Response('Please restart the code')


if __name__ == "__main__":
    # This file should never be run
    pass
