import SecondSight
from flask import Flask
import threading


def startFlask():
    app = Flask(__name__)
    SecondSight.webserver.DEATHSTARE.start(app)
    SecondSight.webserver.ApriltagAPI.start(app)
    SecondSight.webserver.Config.start(app)
    SecondSight.webserver.GamePieceAPI.start(app)
    SecondSight.webserver.Picker.start(app)
    threading.Thread(target=app.run, kwargs={'host': "0.0.0.0"}).start()
    return app
