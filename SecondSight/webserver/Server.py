import SecondSight
from flask import Flask
from flask_socketio import SocketIO
import threading


def startFlask():
    app = Flask(__name__)
    socketio=SocketIO(app)
    SecondSight.webserver.DEATHSTARE.start(app)
    SecondSight.webserver.ApriltagAPI.start(app)
    SecondSight.webserver.Config.start(app)
    SecondSight.webserver.GamePieceAPI.start(app)
    SecondSight.webserver.MainPage.start(app,socketio)
    threading.Thread(target=socketio.run, args=[app], kwargs={'host': "0.0.0.0"}).start()
    return app
