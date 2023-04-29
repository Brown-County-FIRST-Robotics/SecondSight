
import unittest
import tempfile
import SecondSight.config

import os
import json
import SecondSight.Cameras

from . import config_helper

class TestCamera(unittest.TestCase):

    def setUp(self):
        self.config_helper = config_helper.TestImageHelper()
        self.config_object = self.config_helper.config_object

    def tearDown(self):
        del self.config_helper

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

    def testCameraFrameFlip(self):
        cameras = SecondSight.Cameras.loadCameras()
        camera = cameras[0]
        camera.update()

        white_pixel = camera.get_frame(flipped=True)[100][924]
        blue_pixel = camera.get_frame(flipped=True)[700][224]


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

    def testCameraHSV(self):
        cameras = SecondSight.Cameras.loadCameras()
        camera = cameras[0]
        camera.update()

        white_pixel = camera.hsv[100][100]
        black_pixel = camera.hsv[200][200]
        blue_pixel = camera.hsv[700][800]


        # There's probably a better way to compare these
        self.assertEqual(white_pixel[0], 0)
        self.assertEqual(white_pixel[1], 0)
        self.assertEqual(white_pixel[2], 255)

        # There's probably a better way to compare these
        self.assertEqual(black_pixel[0], 0)
        self.assertEqual(black_pixel[1], 0)
        self.assertEqual(black_pixel[2], 0)

        # There's probably a better way to compare these
        self.assertEqual(blue_pixel[0], 112)
        self.assertEqual(blue_pixel[1], 236)
        self.assertEqual(blue_pixel[2], 192)
