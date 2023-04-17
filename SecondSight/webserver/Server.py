import SecondSight.webserver.DEATHSTARE
import SecondSight.webserver.ApriltagAPI
import SecondSight.webserver.Config
import SecondSight
from flask import Flask
import threading


def startFlask():
    config = SecondSight.config.Configuration()

    app = Flask(__name__)
    app.cameras = SecondSight.Cameras.loadCameras()
    app.apriltags = []
    SecondSight.webserver.DEATHSTARE.start(app)
    SecondSight.webserver.ApriltagAPI.start(app)
    SecondSight.webserver.Config.start(app)
    SecondSight.webserver.GamePieceAPI.start(app)
    threading.Thread(target=app.run, kwargs={'host': "0.0.0.0"}).start()
    return app