#!/usr/bin/env python

import uvicorn
import SecondSight.backend.server
import SecondSight.frontend.server
import SecondSight.Cameras
from threading import Thread
import time

def worker():
        
    config = SecondSight.config.Configuration()
    config.set_path("config.json")
    
    while True:
        SecondSight.Cameras.CameraManager.updateAll()
        time.sleep(0.1)
    pass

def frontend_cli():
    # Launch the frontend
    app = SecondSight.frontend.server.app
    app.run()

def febe_cli():
    # Launch the frontend and backends

    frontend_app = SecondSight.frontend.server.app
    thread = Thread(target=frontend_app.run)
    thread.setDaemon(True)
    thread.start()

    backend_cli()

def backend_cli():

    # We spawn a worker thread for background tasks
    thread = Thread(target=worker)
    # Set the thread to be a daemon so it properly exits
    thread.setDaemon(True)
    thread.start()

    # Run the FastAPI server
    app = SecondSight.backend.server.app
    uvicorn.run(app)

if __name__ == "__main__":
    # This file should never be run
    main_cli()
