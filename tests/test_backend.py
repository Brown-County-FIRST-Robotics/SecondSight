
import unittest
import tempfile
import os
import json
from fastapi.testclient import TestClient
import SecondSight.backend.server

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
