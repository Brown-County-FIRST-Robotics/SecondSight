#!/usr/bin/env python

import uvicorn
import SecondSight.backend.server

def main_cli():
    app = SecondSight.backend.server.app
    uvicorn.run(app)

if __name__ == "__main__":
    # This file should never be run
    pass
