#!/usr/bin/env python

import logging
import numpy as np
import cv2
import math
import SecondSight
import networktables


# use this for calibrating the color detector
# pass in frame
# pass in range from center of image that you want to sample
# returns average color is an array
def averageColor(frame, sampleRange):
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    height = len(hsv)
    width = len(hsv[0])
    x = int(width / 2) - sampleRange
    y = int(height / 2) - sampleRange
    hSum = 0
    sSum = 0
    vSum = 0
    for i in range(x, x + 2 * sampleRange):
        for j in range(y, y + 2 * sampleRange):
            hSum += hsv[j][i][0]
            sSum += hsv[j][i][1]
            vSum += hsv[j][i][2]
    averageColor = [ hSum / (4 * sampleRange * sampleRange), sSum / (4 * sampleRange * sampleRange), vSum / (4 * sampleRange * sampleRange) ]
    return averageColor


def findCube2023(frame, cube_color):
    logging.info("findObject()")
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    cube_object_mask = cv2.inRange(hsv, cube_color[0], cube_color[1])
    cube_res = cv2.bitwise_and(frame, frame, mask=cube_object_mask)
    cube_contours, _ = cv2.findContours(cv2.cvtColor(cube_res, cv2.COLOR_BGR2GRAY), cv2.RETR_TREE,
                                        cv2.CHAIN_APPROX_SIMPLE)

    res = []
    for contour in cube_contours:
        pos, dims, theta = cv2.minAreaRect(contour)
        res.append(GamePiece(pos[0], pos[1], dims[0], dims[1], theta, 'cube2023'))
    return res


def findCone2023(frame, cone_color):
    logging.info("findCone2023()")
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    cube_object_mask = cv2.inRange(hsv, cone_color[0], cone_color[1])
    cube_res = cv2.bitwise_and(frame, frame, mask=cube_object_mask)
    cube_contours, _ = cv2.findContours(cv2.cvtColor(cube_res, cv2.COLOR_BGR2GRAY), cv2.RETR_TREE,
                                        cv2.CHAIN_APPROX_SIMPLE)
    res = []
    for contour in cube_contours:
        pos, dims, theta = cv2.minAreaRect(contour)
        res.append(GamePiece(pos[0], pos[1], dims[0], dims[1], theta, 'cone2023'))
    return res


cube_size = 10  # CM


# GamePiece - can represent a cone or a cube
class GamePiece:
    def __init__(self, x, y, width, height, theta, piece):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.theta = theta
        self.piece = piece
        self.pitch = None
        self.yaw = None
        self.roll = None
        self.left_right = None
        self.distance = None
        self.up_down = None
        self.rms = None

    # The cube should ideally be at the same height as the camera
    def calcRealPos(self, camera_matrix, dist):  # TODO:test
        if self.piece == 'cube2023':
            box = cv2.boxPoints(((self.x, self.y), (self.width, self.height), self.theta))
            image_points = np.array(box).reshape(1, 4, 2)

            ob_pt1 = [-cube_size / 2, -cube_size / 2, -cube_size / 2]
            ob_pt2 = [cube_size / 2, -cube_size / 2, -cube_size / 2]
            ob_pt3 = [cube_size / 2, cube_size / 2, cube_size / 2]
            ob_pt4 = [-cube_size / 2, cube_size / 2, cube_size / 2]
            ob_pts = ob_pt1 + ob_pt2 + ob_pt3 + ob_pt4
            object_pts = np.array(ob_pts).reshape(4, 3)
            good, rotation_vector, translation_vector, self.rms = cv2.solvePnPGeneric(object_pts, image_points,
                                                                                      camera_matrix,
                                                                                      dist,
                                                                                      flags=cv2.SOLVEPNP_ITERATIVE)
            assert good, 'something went wrong with solvePnP'

            self.pitch, self.yaw, self.roll = [float(i) for i in rotation_vector[0] * 180 / math.pi]

            self.left_right = translation_vector[0][0]
            self.up_down = translation_vector[0][1]
            self.distance = translation_vector[0][2]

    def drawBoundRect(self, frame, color):  # TODO: test
        box = cv2.boxPoints((self.x, self.y, self.width, self.height, self.theta))
        box = np.int0(box)
        cv2.drawContours(frame, [box], 0, color, 2)


def postGamePieces(tb: networktables.NetworkTable, cams, obj_types: [str]):
    res = {}
    if obj_types is not None:
        for obj in obj_types:
            dets = []
            res[obj] = []
            for i, cam in enumerate(cams): 
                if obj == 'cube2023':
                    det = findCube2023(cam.frame, ((50, 0, 200), (230, 50, 255)))
                    for ii in det:
                        ii.calcRealPos(cam.camera_matrix, None)
                        res[obj].append({
                            "left_right": ii.left_right,
                            "up_down": ii.up_down,
                            "distance": ii.distance,
                            "yaw": ii.yaw,
                            "pitch": ii.pitch,
                            "roll": ii.roll,
                            "rms": ii.rms,
                            "camera": i
                        })
                        dets += [ii.left_right, ii.up_down, ii.distance, ii.yaw, ii.pitch, ii.roll, i]
                if obj == 'cone2023':
                    det = findCone2023(cam.frame, ((0, 0, 0), (255, 100, 100)))
                    for ii in det:
                        res[obj].append({
                            "x": ii.x,
                            "y": ii.y,
                            "width": ii.width,
                            "height": ii.height,
                            "theta": ii.theta,
                            "camera": i
                        })
                        dets += [ii.x, ii.y, ii.width, ii.height, ii.theta, i]
            tb.putNumberArray(obj, dets)
    return res


# This function is now very broken
# Color picker
# This function gets called by the /video_feed route below
def gen_preview_picker(camera):  # generate frame by frame from camera
    logging.debug("Vision.gen_frames_picker")

    config = SecondSight.config.Configuration()

    col = config.get_value("cube_hsv")

    cube = GamePiece()

    lower = [col[0] - 5, col[1] - 100, col[2] - 100]
    upper = [col[0] + 5, col[1] + 100, col[2] + 100]

    for i in range(len(lower)):
        if lower[i] < 0:
            lower[i] = 0
        if lower[i] > 255:
            lower[i] = 255

        if upper[i] < 0:
            upper[i] = 0
        if upper[i] > 255:
            upper[i] = 255

    cube.setLowerColor(np.array(lower, dtype=np.uint8))
    cube.setUpperColor(np.array(upper, dtype=np.uint8)) 
    cube.setMinRatio(3.0 / 5.0)
    cube.setMaxRatio(5.0 / 3.0)

    currentFrame = 0

    # We want to loop this forever
    while True:
        frame = camera.get_frame()
       
#        if camera.frame_count == currentFrame:
#            continue     
#        currentFrame = camera.frame_count

        cube.findObject(frame)  
        
        cv2.rectangle(frame, cube.getLowerLeft(), cube.getUpperRight(), (255, 0, 0), 2)
        ret, jpeg = cv2.imencode('.jpg', frame)
        data = jpeg.tobytes()

        # Return the image to the browser
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + data + b'\r\n')  # concat frame one by one and show result

if __name__ == "__main__":
    pass
