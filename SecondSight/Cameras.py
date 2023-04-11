#!/usr/bin/env python

import logging
import cv2
import time
import threading
import numpy as np


class Camera:
    def __init__(self, device, calibration, position, role):
        logging.debug(f"camera init {device}")
        self.frame = None
        self._hsv = None
        self._gray = None

        self.id = None
        self.frame_count = 0
        self.last_frame_count = 0
        self.device = device
        self.camera = cv2.VideoCapture(device)
        self.role = role

    def update(self):
        success, self.frame=self.camera.read()
        if self.frame is None or not success:
            logging.critical("Camera Read Failed")
        self._hsv=None
        self._gray=None

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

#  I removed this code for now, we can fix it later
#    def get_jpg_bytes(self, flipped=False):
#        # Let's block on this call if we alredy returned this frame
#        self.last_frame_count = self.frame_count
#        logging.debug("camera.get_jpg_bytes")
#        frame = self.get_frame(flipped)
#
#        ret, buffer = cv2.imencode('.jpg', frame)
#        jpg = buffer.tobytes()
#        return jpg


if __name__ == "__main__":
    pass
