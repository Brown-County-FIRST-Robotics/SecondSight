import SecondSight.webserver.DEATHSTARE
import SecondSight.webserver.ApriltagAPI
import SecondSight.webserver.Config
from flask import Flask
import threading


def startFlask(cameras):
    app = Flask(__name__)
    app.cameras = cameras
    app.apriltags = []
    SecondSight.webserver.DEATHSTARE.start(app)
    SecondSight.webserver.ApriltagAPI.start(app)
    SecondSight.webserver.Config.start(app)
    threading.Thread(target=app.run, kwargs={'host': "0.0.0.0"}).start()
    return app