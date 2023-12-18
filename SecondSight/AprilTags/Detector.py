import logging
import math
import apriltag
import cv2
import numpy as np
import SecondSight
from SecondSight.utils import LogMe


class PoseEstimate:
    def __init__(self, yaw, pitch, roll, y, z, x, tagid):
        self.yaw = yaw
        self.pitch = pitch
        self.roll = roll
        self.y = y
        self.z = z
        self.x = x
        self.tagID = tagid

    def __repr__(self):
        if self.tagID is not None:
            return f'RelativePoseEstimate({self.yaw}, {self.pitch}, {self.roll}, {self.y}, {self.z}, {self.x}, {self.tagID})'
        else:
            return f'FieldPoseEstimate({self.yaw}, {self.pitch}, {self.roll}, {self.y}, {self.z}, {self.x})'


@LogMe
def getCoords(img, valid_tags=range(1, 9)):
    if img is None:
        return []
    if len(img.shape) != 2:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    options = apriltag.DetectorOptions(families='tag16h5',
                                       border=1,
                                       nthreads=1,
                                       quad_decimate=1.0,
                                       quad_blur=0.0,
                                       refine_edges=True,
                                       refine_decode=False,
                                       refine_pose=True,
                                       debug=False,
                                       quad_contours=True)
    # Create a detector with given options
    detector = apriltag.Detector(options)
    # Find the apriltags
    detection_results = detector.detect(img)
    detections = []
    if len(detection_results) > 0:  # Check if there are any apriltags
        for detection in detection_results:
            # Check if apriltag is allowed
            if detection.tag_id not in valid_tags:
                continue
            if detection.hamming != 0:
                continue
            detections.append(([list(i) for i in detection.corners], detection.tag_id))
    return detections


@LogMe
def getRelativePosition(det, camera_matrix, dist_coefficients):
    image_points = np.array(det[0]).reshape(1, 4, 2)

    ob_pt1 = [-SecondSight.AprilTags.Positions.tag_size / 2, -SecondSight.AprilTags.Positions.tag_size / 2, 0.0]
    ob_pt2 = [SecondSight.AprilTags.Positions.tag_size / 2, -SecondSight.AprilTags.Positions.tag_size / 2, 0.0]
    ob_pt3 = [SecondSight.AprilTags.Positions.tag_size / 2, SecondSight.AprilTags.Positions.tag_size / 2, 0.0]
    ob_pt4 = [-SecondSight.AprilTags.Positions.tag_size / 2, SecondSight.AprilTags.Positions.tag_size / 2, 0.0]
    ob_pts = ob_pt1 + ob_pt2 + ob_pt3 + ob_pt4
    object_pts = np.array(ob_pts).reshape(4, 3)

    # Solve for rotation and translation
    good, rotation_vector, translation_vector, _ = cv2.solvePnPGeneric(object_pts, image_points,
                                                                       camera_matrix,
                                                                       dist_coefficients,
                                                                       flags=cv2.SOLVEPNP_IPPE_SQUARE)
    assert good, 'something went wrong with solvePnP'

    # Map rotation_vector
    pitch, yaw, roll = [float(i) for i in rotation_vector[0]]

    left_right = translation_vector[0][0]
    up_down = translation_vector[0][1]
    distance = translation_vector[0][2]
    return PoseEstimate(yaw, pitch, roll, left_right, up_down, distance, det[1])


@LogMe
def getFieldPosition(dets, camera_matrix, dist_coefficients):
    image_points = np.array([i[0] for i in dets]).reshape(1, 4 * len(dets), 2)

    object_pts = np.array([SecondSight.AprilTags.Positions.apriltagFeatures['2023'][str(i[1])] for i in dets])  # TODO: make year configured

    # Solve for rotation and translation
    good, rotation_vector, translation_vector, _ = cv2.solvePnPGeneric(object_pts, image_points,
                                                                       camera_matrix,
                                                                       dist_coefficients,

                                                                       flags=cv2.SOLVEPNP_IPPE)
    assert good, 'something went wrong with solvePnP'


    # Map rotation_vector
    pitch, yaw, roll = [float(i) for i in rotation_vector[0]]

    y = -translation_vector[0][0]
    z = -translation_vector[0][1]
    x = translation_vector[0][2]

    pitch2, yaw2, roll2 = [float(i) for i in rotation_vector[-1]]

    y2 = -translation_vector[-1][0]
    z2 = -translation_vector[-1][1]
    x2 = translation_vector[-1][2]

    return PoseEstimate(-yaw, pitch, -roll, y, z, x, None),PoseEstimate(-yaw2, pitch2, -roll2, y2, z2, x2, None)


if __name__ == "main":
    pass
else:
    pass
