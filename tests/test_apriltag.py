import math
import unittest
import tempfile
import SecondSight
import tests.make_apriltag_cases

import cv2
import os
import json
import time
import numpy as np


class TestCamera(unittest.TestCase):
    def testApriltagPose(self):
        focal_length = 500
        principal_point = (640 / 2, 480 / 2)
        camera_matrix = np.array([
            [focal_length, 0, principal_point[0]],
            [0, focal_length, principal_point[1]],
            [0, 0, 1]
        ], dtype=np.float32)
        cases = 0
        total_time = 0
        for img, _, _, id in tests.make_apriltag_cases.genImages():
            start_time = time.time()
            coords=SecondSight.AprilTags.Detector.getCoords(img,'2023')
            self.assertIsNotNone(coords)
            self.assertEqual(len(coords), 1 if id != 9 else 0, f"Wrong number of apriltags detected. Expected {1 if id != 9 else 0}, got {len(coords)}")
            if len(coords) == 1:
                self.assertEqual(coords[0][1], id, f"Wrong tag id. Expected {id}, got {coords[0][1]}")
                dets = SecondSight.AprilTags.Detector.getRelativePosition(coords[0], camera_matrix, None, '2023')
            total_time += time.time() - start_time
            cases += 1
        print()
        print(f"Average time: {1000 * total_time / cases} ms")
