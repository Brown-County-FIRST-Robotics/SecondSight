#!/usr/bin/env python

import logging
import cv2
import time
import threading
import SecondSight
import numpy as np
from typing import List

class Camera:
    """
    Class represenging a camera object for interacting with OpenCV.
    This object will read from the camera hardware and return frame information
    in formats OpenCV expects.
    """

    # Calibration data shoudl be in the format of
    # calibration: {'camera_matrix': %%, 'dist':%%, 'calibration_res':%%, 'processing_res':%%}

    def __init__(self, device, calibration, position, role):
        """Camera constructor

        :param device: The camera device such as '/dev/video0'
        :param calibration: Camera calibration data
        :param position: The camera position on the robot, not currently used
        :param role: The role of the camera in the larger system

        :return:
        """

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
            processing_resolution = np.array(calibration['processing_res'])
            if calibration['dist'] is not None:
                dist_coefficients = np.array(calibration['dist'])
                self.camera_matrix, roi = cv2.getOptimalNewCameraMatrix(raw_camera_matrix, dist_coefficients,
                                                                        tuple(video_size), 0,
                                                                        tuple(processing_resolution))
                self.map1, self.map2 = cv2.initUndistortRectifyMap(raw_camera_matrix, dist_coefficients, None,
                                                                   self.camera_matrix,
                                                                   tuple(processing_resolution), cv2.CV_16SC2)
            else:
                self.map1 = None
                self.map2 = None
                self.camera_matrix = raw_camera_matrix
        else:
            self.map1=None
            self.map2=None
            self.camera_matrix=None
            assert role != 'apriltag' and role != '*', f'For the role to be "{role}", a calibration is required'

    def update(self):
        """Read a new camera frame from the camera

        :return:
        """

        success, frame = self.camera.read()
        if frame is None or not success:
            logging.critical("Camera Read Failed")
            return 
        self.uncalibrated = frame.copy() 
        if self.map2 is not None:
            frame = cv2.remap(frame, self.map1, self.map2, cv2.INTER_CUBIC)
        self.frame = frame
        self._hsv = None
        self._gray = None
        self._bytes = None
        self._bytes_uncalibrated = None

    def get_frame(self, flipped=False):
        """Return the current frame
        
        :param flipped: Defaults to false. Mirror the image if true
        
        :return: OpenCV frame data
        """
        if flipped:
            return cv2.flip(self.frame, 1)
        else:
            return self.frame

    @property
    def hsv(self):
        "Return the current frame HSV data"
        logging.debug("camera.get_hsv")
        if self._hsv is None:
            self._hsv = cv2.cvtColor(self.frame, cv2.COLOR_BGR2HSV)
        return self._hsv

    @property
    def gray(self):
        "return the current frame in grayscale"
        logging.debug("camera.get_gray")
        if self.frame is None:
            return None
        if self._gray is None:
            self._gray = cv2.cvtColor(self.frame, cv2.COLOR_BGR2GRAY)
        return self._gray

    @property
    def height(self):
        "return the height of the image"
        logging.debug("camera.get_height")
        return len(self.frame)

    @property
    def width(self):
        "return the width of the image"
        logging.debug("camera.get_width")
        return len(self.frame[0])

    def get_bytes(self, uncalibrated=False):
        """Return the current frame as a byte array of JPG data

        :param uncalibrated: Defaults to false

        :return: Byte array of JPG data
        """

        # TODO: This is confusing. We should probably call it "calibrated"
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


class CameraLoader:

    camera_cache = []

    @classmethod
    def loadCameras(cls) -> List[Camera]:
        """
        Initialize the cameras as defined in the configuration file
        """

        if len(cls.camera_cache) == 0:
            # Only load the cameras once, use the cache after this
            config = SecondSight.config.Configuration()
            for cam_config in config.get_value('cameras'):
                cls.camera_cache.append(Camera(cam_config['port'], cam_config['calibration'], cam_config['pos'], cam_config['role']))
        
        return cls.camera_cache

    @classmethod
    def getCamera(cls, cam_index) -> Camera:
        """
        Return a camera object by its index
        """

        cls.loadCameras()
        return cls.camera_cache[cam_index]

    @classmethod
    def updateAll(cls) -> None:
        """
        Update all the cameras
        """
        for cam in cls.loadCameras():
            cam.update()


if __name__ == "__main__":
    pass
