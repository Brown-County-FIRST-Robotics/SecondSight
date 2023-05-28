#!/usr/bin/env python

import uvicorn
import SecondSight.frontend.server

def main_cli():
    app = SecondSight.frontend.server.app
    app.run()

if __name__ == "__main__":
    # This file should never be run
    main_cli()