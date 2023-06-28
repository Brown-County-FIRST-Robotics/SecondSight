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


if __name__ == "__main__":
    pass
