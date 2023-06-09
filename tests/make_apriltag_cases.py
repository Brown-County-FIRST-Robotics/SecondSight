import json
import logging
import os
import random
import shutil

import cv2
import numpy as np

apriltags = [
    [0, 0, 1, 0, 1, 1, 1, 0, 1, 0, 1, 0, 0, 1, 0, 1],
    [0, 0, 1, 1, 0, 1, 0, 0, 0, 1, 1, 0, 1, 0, 1, 0],
    [0, 1, 0, 0, 0, 1, 0, 1, 1, 0, 1, 1, 1, 0, 0, 1],
    [0, 1, 1, 1, 1, 0, 0, 1, 1, 0, 1, 0, 0, 1, 1, 0],
    [0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 0, 1, 0, 1, 1],
    [1, 0, 1, 1, 0, 0, 1, 1, 0, 1, 0, 1, 1, 0, 0, 0],
    [1, 1, 1, 0, 0, 1, 1, 1, 0, 1, 0, 0, 0, 1, 0, 1],
    [1, 1, 1, 1, 1, 1, 1, 0, 0, 1, 0, 1, 1, 0, 0, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 0, 0, 1]  # This is a fake tag; it should not be detected if check_hamming=True
]


def genImage(tvec, rvec, tagid, size):
    # Generate a black image
    img = np.zeros(tuple(size + tuple([3])), dtype=np.uint8)
    img[:, :] = (255, 0, 20)
    k = 2.54
    # Define the rectangle corners in 3D space
    pixel_pos = [
        [[-4 * k, 3 * k, 0], [-4 * k, 4 * k, 0], [4 * k, 4 * k, 0], [4 * k, 3 * k, 0]],
        [[-4 * k, -3 * k, 0], [-4 * k, -4 * k, 0], [4 * k, -4 * k, 0], [4 * k, -3 * k, 0]],
        [[-4 * k, -3 * k, 0], [-3 * k, -3 * k, 0], [-3 * k, 3 * k, 0], [-4 * k, 3 * k, 0]],
        [[4 * k, -3 * k, 0], [3 * k, -3 * k, 0], [3 * k, 3 * k, 0], [4 * k, 3 * k, 0]],
        [[-3 * k, 2 * k, 0], [-3 * k, 3 * k, 0], [3 * k, 3 * k, 0], [3 * k, 2 * k, 0]],
        [[-3 * k, -2 * k, 0], [-3 * k, -3 * k, 0], [3 * k, -3 * k, 0], [3 * k, -2 * k, 0]],
        [[-3 * k, -2 * k, 0], [-2 * k, -2 * k, 0], [-2 * k, 2 * k, 0], [-3 * k, 2 * k, 0]],
        [[3 * k, -2 * k, 0], [2 * k, -2 * k, 0], [2 * k, 2 * k, 0], [3 * k, 2 * k, 0]],

        [[-2 * k, -2 * k, 0], [-2 * k, -1 * k, 0], [-1 * k, -1 * k, 0], [-1 * k, -2 * k, 0]],
        [[-1 * k, -2 * k, 0], [-1 * k, -1 * k, 0], [0 * k, -1 * k, 0], [0 * k, -2 * k, 0]],
        [[0 * k, -2 * k, 0], [0 * k, -1 * k, 0], [1 * k, -1 * k, 0], [1 * k, -2 * k, 0]],
        [[1 * k, -2 * k, 0], [1 * k, -1 * k, 0], [2 * k, -1 * k, 0], [2 * k, -2 * k, 0]],

        [[-2 * k, -1 * k, 0], [-2 * k, 0 * k, 0], [-1 * k, 0 * k, 0], [-1 * k, -1 * k, 0]],
        [[-1 * k, -1 * k, 0], [-1 * k, 0 * k, 0], [0 * k, 0 * k, 0], [0 * k, -1 * k, 0]],
        [[0 * k, -1 * k, 0], [0 * k, 0 * k, 0], [1 * k, 0 * k, 0], [1 * k, -1 * k, 0]],
        [[1 * k, -1 * k, 0], [1 * k, 0 * k, 0], [2 * k, 0 * k, 0], [2 * k, -1 * k, 0]],

        [[-2 * k, 0 * k, 0], [-2 * k, 1 * k, 0], [-1 * k, 1 * k, 0], [-1 * k, 0 * k, 0]],
        [[-1 * k, 0 * k, 0], [-1 * k, 1 * k, 0], [0 * k, 1 * k, 0], [0 * k, 0 * k, 0]],
        [[0 * k, 0 * k, 0], [0 * k, 1 * k, 0], [1 * k, 1 * k, 0], [1 * k, 0 * k, 0]],
        [[1 * k, 0 * k, 0], [1 * k, 1 * k, 0], [2 * k, 1 * k, 0], [2 * k, 0 * k, 0]],

        [[-2 * k, 1 * k, 0], [-2 * k, 2 * k, 0], [-1 * k, 2 * k, 0], [-1 * k, 1 * k, 0]],
        [[-1 * k, 1 * k, 0], [-1 * k, 2 * k, 0], [0 * k, 2 * k, 0], [0 * k, 1 * k, 0]],
        [[0 * k, 1 * k, 0], [0 * k, 2 * k, 0], [1 * k, 2 * k, 0], [1 * k, 1 * k, 0]],
        [[1 * k, 1 * k, 0], [1 * k, 2 * k, 0], [2 * k, 2 * k, 0], [2 * k, 1 * k, 0]],
    ]
    pixel_val = [
                    1, 1, 1, 1,  # outer deadzone
                    0, 0, 0, 0,  # inner deadzone
                ] + apriltags[tagid - 1]

    # Project the rectangle corners onto the image plane
    focal_length = 500
    principal_point = (size[1] / 2, size[0] / 2)
    camera_matrix = np.array([
        [focal_length, 0, principal_point[0]],
        [0, focal_length, principal_point[1]],
        [0, 0, 1]
    ], dtype=np.float32)

    # pitch,yaw,roll
    # lr,ud,dist
    rvec = np.array(rvec, dtype=np.float32)
    tvec = np.array(tvec, dtype=np.float32)
    for pts, color in zip(pixel_pos, pixel_val):
        projected_points, _ = cv2.projectPoints(np.array([np.array(i) for i in pts], dtype=np.float32),
                                                np.deg2rad(rvec), tvec, camera_matrix, None)

        # Draw the rectangle on the image
        points = projected_points.astype(np.int32).reshape((-1, 2))
        cv2.fillConvexPoly(img, points, (255, 255, 255) if color else (0, 0, 0))
    return img


# Save the image to a PNG file
def generateImg(rvec, tvec, id):
    img = genImage(tvec, rvec, id, (480, 640))
    cv2.imshow('Output Image', img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    cv2.imwrite('april.png', img)


def genImages():
    for i in range(1, 10):
        yield genImage([1, -4, 30], [5, 45, 90], i, (480, 640)), [5, 45, 90], [1, -4, 30], i
        yield genImage([-1, 4, 35], [-5, -45, -90], i, (480, 640)), [-5, -45, -90], [-1, 4, 35], i


def displayImages():
    for i in genImages():
        cv2.imshow(f'Output Image rvec:{i[1]} tvec:{i[2]} id:{i[3] if i[3] != 9 else "invalid"}', i[0])
        cv2.waitKey(0)
        cv2.destroyAllWindows()
