#!/usr/bin/env python

import logging
import cv2
import time
import threading
import SecondSight.config
import numpy as np


class Camera:
    # calibration: {'camera_matrix': %%, 'dist':%%, 'calibration_res':%%, 'processing_res':%%}
    def __init__(self, device, calibration, position, role):
        logging.debug(f"camera init {device}")
        self.frame = None
        self._hsv = None
        self._gray = None
        self.uncalibrated = None
        self._bytes = None
        self._bytes_uncalibrated = None


        self.id = None
        self.frame_count = 0
        self.last_frame_count = 0
        self.device = device
        self.camera = cv2.VideoCapture(device)
        self.role = role
        self.pos=position

        if calibration is not None:
            video_size = tuple(calibration["calibration_res"])
            self.camera.set(cv2.CAP_PROP_FRAME_WIDTH, video_size[0])
            self.camera.set(cv2.CAP_PROP_FRAME_HEIGHT, video_size[1])
            test_video_size = (self.camera.get(cv2.CAP_PROP_FRAME_WIDTH), self.camera.get(cv2.CAP_PROP_FRAME_HEIGHT))
            assert tuple(test_video_size) == tuple(video_size), 'camera resolution didnt set'

            raw_camera_matrix = np.array(calibration['camera_matrix'])
            dist_coefficients = np.array(calibration['dist'])
            processing_resolution = np.array(calibration['processing_res'])

            self.camera_matrix, roi = cv2.getOptimalNewCameraMatrix(raw_camera_matrix, dist_coefficients, tuple(video_size), 0,tuple(processing_resolution))
            self.map1, self.map2 = cv2.initUndistortRectifyMap(raw_camera_matrix, dist_coefficients, None, self.camera_matrix,
                                                 tuple(processing_resolution), cv2.CV_16SC2)
        else:
            self.map1=None
            self.map2=None
            self.camera_matrix=None
            assert role != 'apriltag' and role != '*', f'For the role to be "{role}", a calibration is required'

    def update(self):
        success, frame = self.camera.read()
        self.uncalibrated = frame.copy()
        if frame is None or not success:
            logging.critical("Camera Read Failed")
        if self.camera_matrix is not None:
            frame = cv2.remap(frame, self.map1, self.map2, cv2.INTER_CUBIC)
        self.frame = frame
        self._hsv = None
        self._gray = None
        self._bytes = None
        self._bytes_uncalibrated = None

    def get_frame(self, flipped=False):
        if flipped:
            return cv2.flip(self.frame, 1)
        else:
            return self.frame

    @property
    def hsv(self):
        logging.debug("camera.get_hsv")
        if self._hsv is None:
            self._hsv = cv2.cvtColor(self.frame, cv2.COLOR_BGR2HSV)
        return self._hsv

    @property
    def gray(self):
        logging.debug("camera.get_gray")
        if self.frame is None:
            return None
        if self._gray is None:
            self._gray = cv2.cvtColor(self.frame, cv2.COLOR_BGR2GRAY)
        return self._gray

    @property
    def height(self):
        logging.debug("camera.get_height")
        return len(self.frame)

    @property
    def width(self):
        logging.debug("camera.get_width")
        return len(self.frame[0])

    def get_bytes(self, uncalibrated=False):
        if not uncalibrated:
            if self._bytes is None:
                logging.debug("camera.get_bytes")
                frame = self.frame
                ret, buffer = cv2.imencode('.jpg', frame)
                self._bytes = buffer.tobytes()
            return self._bytes
        else:
            if self._bytes_uncalibrated is None:
                logging.debug("camera.get_bytes")
                frame = self.uncalibrated
                ret, buffer = cv2.imencode('.jpg', frame)
                self._bytes_uncalibrated = buffer.tobytes()
            return self._bytes_uncalibrated


def loadCameras(config):
    cameras=[]
    for cam_config in config.get_value('cameras'):
        cameras.append(SecondSight.Cameras.Camera(cam_config['port'], cam_config['calibration'], cam_config['pos'], cam_config['role']))
    return cameras


if __name__ == "__main__":
    pass
