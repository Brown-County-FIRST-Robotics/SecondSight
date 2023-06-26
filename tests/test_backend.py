
import unittest
import tempfile
import os
import json
from fastapi.testclient import TestClient
import SecondSight.backend.server
import SecondSight.Cameras

from . import config_helper

class TestBackend(unittest.TestCase):

    def setUp(self):
        self.config_helper = config_helper.TestImageHelper()
        self.config_object = self.config_helper.config_object

        self.app = SecondSight.backend.server.app
        self.client = TestClient(self.app)

    def tearDown(self):
        del self.config_helper

    def testRoot(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"application": "SecondSight"})

    def testAllConfig(self):

        config_data = self.config_object.get_all()

        response = self.client.get("/config")
        self.assertEqual(response.status_code, 200)

        json_resp = response.json()
        self.assertEqual(json_resp, config_data)

    def testOneConfig(self):
        response = self.client.get("/config/nt_dest")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), "127.0.0.1")

        response = self.client.get("/config/cube_hsv")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), [150, 138, 121])
    
    def testSetConfig(self):
        response = self.client.post("/config", json={"nt_dest": "127.0.0.2"})
        self.assertEqual(response.status_code, 200)

        response = self.client.get("/config/nt_dest")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), "127.0.0.2")

    def testGetCamerasAPI(self):
        response = self.client.get("/get_cameras")
        self.assertEqual(len(response.json()), 1)
        self.assertEqual(response.json()[0], '0')

#    def testStreamImage(self):
#        # The stream never returns, we can't test this right now
#
#        cam = SecondSight.Cameras.getCamera(0)
#        cam.update()
#        response = self.client.get("/camera/0")
#        self.assertEqual(response.status_code, 200)
