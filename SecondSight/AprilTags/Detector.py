import logging
import math
import apriltag
import cv2
import numpy as np
import SecondSight
from SecondSight.utils import LogMe,Quaternion


class PoseEstimate:
    def __init__(self, rotation: Quaternion, x, y, z, tagid, rms):
        self.rotation: Quaternion = rotation
        self.y = y
        self.z = z
        self.x = x
        self.tagID = tagid
        self.rms=rms

    def __repr__(self):
        if self.tagID is not None:
            return f'RelativePoseEstimate({self.rotation.w}, {self.rotation.x}, {self.rotation.y}, {self.rotation.z}, {self.x}, {self.y}, {self.z}, {self.tagID}, {self.rms})'
        else:
            return f'FieldPoseEstimate({self.rotation.w}, {self.rotation.x}, {self.rotation.y}, {self.rotation.z}, {self.x}, {self.y}, {self.z}, {self.rms})'


@LogMe
def getCoords(img, year, valid_tags=range(1, 9)):
    if img is None:
        return []
    if len(img.shape) != 2:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    options = apriltag.DetectorOptions(families='tag16h5' if year=='2023' else 'tag36h11',
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
def getRelativePosition(det, camera_matrix, dist_coefficients, year):
    image_points = np.array(det[0]).reshape(1, 4, 2)

    ob_pt1 = [-SecondSight.AprilTags.Positions.tag_size[year] / 2, -SecondSight.AprilTags.Positions.tag_size[year] / 2, 0.0]
    ob_pt2 = [SecondSight.AprilTags.Positions.tag_size[year] / 2, -SecondSight.AprilTags.Positions.tag_size[year] / 2, 0.0]
    ob_pt3 = [SecondSight.AprilTags.Positions.tag_size[year] / 2, SecondSight.AprilTags.Positions.tag_size[year] / 2, 0.0]
    ob_pt4 = [-SecondSight.AprilTags.Positions.tag_size[year] / 2, SecondSight.AprilTags.Positions.tag_size[year] / 2, 0.0]
    ob_pts = ob_pt1 + ob_pt2 + ob_pt3 + ob_pt4
    object_pts = np.array(ob_pts).reshape(4, 3)

    # Solve for rotation and translation
    good, rotation_vector, translation_vector, rms = cv2.solvePnPGeneric(object_pts, image_points,
                                                                         camera_matrix,
                                                                         dist_coefficients,
                                                                         flags=cv2.SOLVEPNP_ITERATIVE)
    assert good, 'something went wrong with solvePnP'

    left_right = translation_vector[0][0]
    up_down = translation_vector[0][1]
    distance = translation_vector[0][2]
    return PoseEstimate(Quaternion.fromOpenCVAxisAngle(rotation_vector[0]), distance, left_right, up_down, det[1], rms[0][0])


@LogMe
def getFieldPosition(dets, camera_matrix, dist_coefficients, year):
    image_points = np.array([i[0] for i in dets]).reshape(1, 4 * len(dets), 2)

    q=SecondSight.AprilTags.Positions.apriltagFeatures[year]
    q2=[q[str(i[1])] for i in dets]
    object_pts = np.array(q2).reshape(1, 4 * len(dets), 3)

    # Solve for rotation and translation
    good, rotation_vector, translation_vector, rms = cv2.solvePnPGeneric(object_pts, image_points,
                                                                         camera_matrix,
                                                                         dist_coefficients,
                                                                         flags=cv2.SOLVEPNP_ITERATIVE)
    assert good, 'something went wrong with solvePnP'


    # Map rotation_vector
    R,_=cv2.Rodrigues(rotation_vector[0])
    R=R.transpose()
    translation_vector2=(R*-1).dot(translation_vector[0])
    rvec,_=cv2.Rodrigues(R)
    y = -translation_vector2[0]
    z = -translation_vector2[1]
    x = translation_vector2[2]
    return PoseEstimate(Quaternion.fromOpenCVAxisAngle(rvec), x, y, z, None, rms[0][0])


if __name__ == "__main__":
    pass
