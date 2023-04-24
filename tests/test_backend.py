
import unittest
from fastapi.testclient import TestClient
import SecondSight.backend.server

class TestBackend(unittest.TestCase):

    def setUp(self):
        self.app = SecondSight.backend.server.app   
        self.client = TestClient(self.app)

    def tearDown(self):
        pass

    def testRoot(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"application": "SecondSight"})
        
