
import SecondSight.config

import tempfile
import os
import json

class TestImageHelper():

    def __init__(self):
        self.tempdir = tempfile.TemporaryDirectory()
        self.config_object = SecondSight.config.Configuration()

        self.config_data = {
            "cameras": [{
                "port": "tests/test-data/test-image.png",
                "calibration": None,
                "role": "conecube",
                "pos": None
            }],
            "nt_dest": "127.0.0.1",
            "cube_hsv": [150, 138, 121]
        }

        self.config_file = os.path.join(self.tempdir.name, "config.json")
        with open(self.config_file, "w") as out_fh:
            json.dump(self.config_data, out_fh)
        self.config_object.set_path(self.config_file)

    def __del__(self):
        self.tempdir.cleanup()

