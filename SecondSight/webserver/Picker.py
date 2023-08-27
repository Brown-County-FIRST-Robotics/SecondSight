import SecondSight
from flask import Flask, render_template, Response, redirect, request, jsonify, Markup


def start(app):
    @app.route('/picker/<int:number>')
    def picker(number):
        args = request.args.to_dict()
        low = (int(args['low_h']), int(args['low_s']), int(args['low_v']))
        upper = (int(args['upper_h']), int(args['upper_s']), int(args['upper_v']))
        # Video streaming route. Put this in the src attribute of an img tag
        return Response(SecondSight.GamePiece.Picker.gen_picker(number, low, upper), mimetype='multipart/x-mixed-replace; boundary=frame')

    @app.route('/picker')
    def picker_page():
        cam_html = ''
        for i in range(len(SecondSight.Cameras.CameraManager.getCameras())):
            cam_html += f'<option value="{i}" selected="selected">{i}</option>'
        return render_template('picker.html', cams=Markup(cam_html))

