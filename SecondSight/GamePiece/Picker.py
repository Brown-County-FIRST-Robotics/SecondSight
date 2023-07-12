import SecondSight
import logging
import cv2
import time
import SecondSight
import numpy as np


def gen_picker(cam_ind, lower_color: tuple[int, int, int], upper_color: tuple[int, int, int]):
    cam = SecondSight.Cameras.CameraManager.getCamera(cam_ind)
    last_frame_time = 0
    framerate = 10
    while True:
        while time.time() - last_frame_time < 1 / framerate:
            time.sleep(0.001)
        frame = cam.frame

        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(hsv, lower_color, upper_color)
        res = cv2.bitwise_and(frame, frame, mask=mask)
        contours, _ = cv2.findContours(cv2.cvtColor(res, cv2.COLOR_BGR2GRAY), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        for contour in contours:
            pos, dims, theta = cv2.minAreaRect(contour)
            box = cv2.boxPoints((pos, dims, theta))
            box = np.int0(box)
            frame = cv2.drawContours(frame, [box], 0, (0, 0, 0), 2)
        # Return the image to the browser
        ret, jpeg = cv2.imencode('.jpg', frame)
        data = jpeg.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + data + b'\r\n')  # concat frame one by one and show result
