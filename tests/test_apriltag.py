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
        tr_threshold = 0.2
        rot_threshold = 0.5
        focal_length = 500
        principal_point = (640 / 2, 480 / 2)
        camera_matrix = np.array([
            [focal_length, 0, principal_point[0]],
            [0, focal_length, principal_point[1]],
            [0, 0, 1]
        ], dtype=np.float32)
        total_rot_err = 0
        total_t_err = 0
        cases = 0
        total_time = 0
        for img, rvec, tvec, id in tests.make_apriltag_cases.genImages():
            start_time = time.time()
            dets = SecondSight.AprilTags.Detector.getPosition(img, camera_matrix, None)
            total_time += time.time() - start_time
            self.assertIsNotNone(dets)
            self.assertEqual(len(dets), 1 if id != 9 else 0, f"Wrong number of apriltags detected. Expected {1 if id != 9 else 0}, got {len(dets)}")
            if len(dets) == 1:
                self.assertEqual(dets[0].tagID, id, f"Wrong tag id. Expected {id}, got {dets[0].tagID}")

                r_err = math.fabs(dets[0].pitch - rvec[0]) + math.fabs(dets[0].yaw - rvec[1]) + math.fabs(dets[0].roll - rvec[2])
                self.assertTrue(r_err < rot_threshold, f"Rotational error exceeds limit. Error was {r_err}, limit is {rot_threshold}")

                t_err = math.fabs(dets[0].left_right - tvec[0]) + math.fabs(dets[0].up_down + tvec[1]) + math.fabs(dets[0].distance - tvec[2])
                self.assertTrue(t_err < tr_threshold, f"Translation error exceeds limit. Error was {t_err}, limit is {tr_threshold}")
                total_t_err += t_err
                total_rot_err += r_err
                cases += 1
        print()
        print(f"Average rot error: {total_rot_err / cases}")
        print(f"Average t error: {total_t_err / cases}")
        print(f"Average time: {1000 * total_time / cases} ms")
