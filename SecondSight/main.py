#!/usr/bin/env python

import sys
import SecondSight.webserver.server

def main_cli():
    app = SecondSight.webserver.server.get_app()
    app.run()

if __name__ == "__main__":
    # This file should never be run
    pass