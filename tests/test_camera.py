
import unittest
import tempfile
import SecondSight.config

import os
import json
import SecondSight.Cameras

class TestCamera(unittest.TestCase):

    def setUp(self):
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

    def tearDown(self):
        self.tempdir.cleanup()

    def testCameraOpen(self):
        cameras = SecondSight.Cameras.loadCameras()
        camera = cameras[0]
        camera.update()

        self.assertEqual(len(cameras), 1)
        self.assertEqual(camera.width, 1024)
        self.assertEqual(camera.height, 1024)

    def testCameraFrame(self):
        cameras = SecondSight.Cameras.loadCameras()
        camera = cameras[0]
        camera.update()

        white_pixel = camera.get_frame()[100][100]
        blue_pixel = camera.get_frame()[700][800]


        # There's probably a better way to compare these
        self.assertEqual(white_pixel[0], 255)
        self.assertEqual(white_pixel[1], 255)
        self.assertEqual(white_pixel[2], 255)

        # There's probably a better way to compare these
        self.assertEqual(blue_pixel[0], 192)
        self.assertEqual(blue_pixel[1], 64)
        self.assertEqual(blue_pixel[2], 14)

    def testCameraGray(self):
        cameras = SecondSight.Cameras.loadCameras()
        camera = cameras[0]
        camera.update()

        black_pixel = camera.gray[200][200]
        white_pixel = camera.gray[100][100]
        blue_pixel = camera.gray[700][800] # Obviously not blue anymore

        self.assertEqual(black_pixel, 0)
        self.assertEqual(white_pixel, 255)
        self.assertEqual(blue_pixel, 64)