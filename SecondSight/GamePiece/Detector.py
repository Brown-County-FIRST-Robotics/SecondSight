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


def findCube2023(frame):
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    cube_object_mask = cv2.inRange(hsv, *SecondSight.GamePiece.PieceConstants.CUBE_2023_COLOR_RANGE)
    cube_res = cv2.bitwise_and(frame, frame, mask=cube_object_mask)
    cube_contours, _ = cv2.findContours(cv2.cvtColor(cube_res, cv2.COLOR_BGR2GRAY), cv2.RETR_TREE,
                                        cv2.CHAIN_APPROX_SIMPLE)

    res = []
    for contour in cube_contours:
        pos, dims, theta = cv2.minAreaRect(contour)
        res.append(SecondSight.GamePiece.Pieces.Cube2023(pos[0], pos[1], dims[0], dims[1], theta))
    return res


def findCone2023(frame):
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    cube_object_mask = cv2.inRange(hsv, *SecondSight.GamePiece.PieceConstants.CONE_2023_COLOR_RANGE)
    cube_res = cv2.bitwise_and(frame, frame, mask=cube_object_mask)
    cube_contours, _ = cv2.findContours(cv2.cvtColor(cube_res, cv2.COLOR_BGR2GRAY), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    res = []
    for contour in cube_contours:
        pos, dims, theta = cv2.minAreaRect(contour)
        res.append(SecondSight.GamePiece.Pieces.Cone2023(pos[0], pos[1], dims[0], dims[1], theta))
    return res


def findGivenPieceType(frame, piece_type):
    if piece_type == 'cube2023':
        return findCube2023(frame)
    elif piece_type == 'cone2023':
        return findCone2023(frame)


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
