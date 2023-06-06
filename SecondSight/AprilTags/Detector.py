# TODO: add tests (use the mock camera code from the sim branch of 1716-2023-robot
import logging
import math
import apriltag
import cv2
import numpy as np
import SecondSight
import concurrent.futures
from typing import List
import networktables

tag_size = 6


class Detection:
    def __init__(self, yaw, pitch, roll, left_right, up_down, distance, rms, tagid):
        self.yaw = yaw
        self.pitch=pitch
        self.roll=roll
        self.left_right = left_right
        self.up_down=up_down
        self.distance = distance
        self.RMSError = rms
        self.tagID = tagid

        self.field_yaw = None
        self.field_x = None
        self.field_y = None

        self.yaw_std = None
        self.left_right_std = None
        self.distance_std = None
        self.error = None

    def calcError(self, error_matrix=None, error_threshold=3000):  # TODO: add error threshold
        if error_matrix is None:
            error_matrix = np.array([  # TODO: add real values
                [1, 1, 1, 1],
                [1, 1, 1, 1],
                [1, 1, 1, 1],
                [1, 1, 1, 1],
            ])
        input_matrix = np.array([  # TODO: rename
            self.yaw,
            self.left_right,
            self.distance,
            self.RMSError
        ])
        self.yaw_std, self.left_right_std, self.distance_std, self.error = [i for i in
                                                                            np.dot(error_matrix, input_matrix).tolist()]
        if self.error > error_threshold:
            logging.info(f'discarded a value (error:{self.error})')

    def json(self, error=False):
        res = {
            "left_right": self.left_right,
            "up_down": self.up_down,
            "distance": self.distance,
            "pitch": self.pitch,
            "yaw": self.yaw,
            "roll": self.roll,
            "tagid": self.tagID
        }
        if error:
            self.calcError()
            res['rms']=self.RMSError
            res['yaw_std']=self.yaw_std
            res['left_right_std'] = self.left_right_std
            res['distance_std'] = self.distance_std
            res['error'] = self.error
        return res

    def calcFieldPos(self, year):
        pos = SecondSight.AprilTags.Positions.apriltagPositions[year][str(self.tagID)]
        camera_theta = 180 + self.yaw + pos[3]
        thetaCA = camera_theta - math.atan(self.left_right / self.distance) * 180 / math.pi
        camera_Y = pos[1] - (math.sqrt(self.left_right ** 2 + self.distance ** 2) * math.sin(thetaCA * math.pi / 180))
        camera_X = pos[0] - (math.sqrt(self.left_right ** 2 + self.distance ** 2) * math.cos(thetaCA * math.pi / 180))
        self.field_x = camera_X
        self.field_y = camera_Y
        self.field_yaw=camera_theta
        return camera_X, camera_Y, camera_theta


def getCoords(img, valid_tags=range(1, 9), check_hamming=True):
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
    detections=[]
    if len(detection_results) > 0:  # Check if there are any apriltags
        for detection in detection_results:
            # Check if apriltag is allowed
            if detection.tag_id not in valid_tags:
                continue
            if detection.hamming != 0:
                continue
            detections.append(([list(i) for i in detection.corners], detection.tag_id))
    return detections


def getPosition(img, camera_matrix, dist_coefficients, valid_tags=range(1, 9), check_hamming=True):
    """
    This function takes an image and returns the position of apriltags in the image

    :param img: The image you want to find apriltags in (must be grayscale)
    :param camera_matrix: The camera's calibration matrix
    :param dist_coefficients: The distortion coefficients of the camera
    :param valid_tags: (Default: 1-9) The apriltags to look for
    :param check_hamming: (Default: True) Checks if the hamming value is 0
    :return: A list of Detection objects, or None if it fails
    :rtype: list(Detection objects), or None if no apriltags are found
    """
    # Check if image is grayscale
    if img is None:
        return []
    detection_results=getCoords(img, valid_tags=valid_tags, check_hamming=check_hamming)
    detections = []
    if len(detection_results) > 0:  # Check if there are any apriltags
        for detection,tagid in detection_results:
            # Check if apriltag is allowed

            image_points = np.array(detection).reshape(1, 4, 2)

            ob_pt1 = [-tag_size / 2, -tag_size / 2, 0.0]
            ob_pt2 = [tag_size / 2, -tag_size / 2, 0.0]
            ob_pt3 = [tag_size / 2, tag_size / 2, 0.0]
            ob_pt4 = [-tag_size / 2, tag_size / 2, 0.0]
            ob_pts = ob_pt1 + ob_pt2 + ob_pt3 + ob_pt4
            object_pts = np.array(ob_pts).reshape(4, 3)

            # Solve for rotation and translation
            good, rotation_vector, translation_vector, rms = cv2.solvePnPGeneric(object_pts, image_points,
                                                                                 camera_matrix,
                                                                                 dist_coefficients,
                                                                                 flags=cv2.SOLVEPNP_ITERATIVE)
            assert good, 'something went wrong with solvePnP'

            # Map rotation_vector
            pitch, yaw, roll = [float(i) for i in rotation_vector[0] * 180 / math.pi]

            left_right = translation_vector[0][0] * 2.54
            up_down = -translation_vector[0][1] * 2.54
            distance = translation_vector[0][2] * 2.54

            logging.info(f'april pos: yaw:{str(yaw)[:5]}, lr:{str(left_right)[:7]}, distance:{str(distance)[:7]}, rms:{rms}, tag:{tagid}')
            detections.append(Detection(yaw, pitch, roll, left_right[0], up_down[0], distance[0], rms[0][0], tagid))
    return detections


# Source: https://math.stackexchange.com/a/1033561
def fuseApriltags(dets: List[Detection], year: str = '2023'):
    assert len(dets) > 1
    if len(dets) > 2:
        dets = dets[:2]
    x1, y1 = SecondSight.AprilTags.Positions.apriltagPositions[year][str(dets[0].tagID)][:2]
    x2, y2 = SecondSight.AprilTags.Positions.apriltagPositions[year][str(dets[1].tagID)][:2]
    d = math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)
    r1 = math.sqrt(dets[0].left_right ** 2 + dets[0].distance ** 2)
    r2 = math.sqrt(dets[1].left_right ** 2 + dets[0].distance ** 2)
    l = (r1 ** 2 - r2 ** 2 + d ** 2) / (2 * d)
    h = math.sqrt(r1 ** 2 - l ** 2)
    k = -1  # or 1
    x = (l / d) * (x2 - x1) + (k * h / d) * (y2 - y1) + x1
    y = (l / d) * (y2 - y1) - (k * h / d) * (x2 - x1) + y1

    theta = math.atan2(x2 - x, y2 - y) - math.atan2(dets[1].left_right, dets[1].distance)
    theta = -90 - theta
    return x, y, theta


class ApriltagManager:
    instance = None

    @classmethod
    def getInst(cls):
        if cls.instance is None:
            cls.instance = ApriltagManager()
        return cls.instance

    def __init__(self):
        self.current_apriltags: List[Detection] = []
        self.april_table = networktables.NetworkTables.getTable('SecondSight').getSubTable('Apriltags')
        self.fetchApriltags()

    def fetchApriltags(self):
        res = []
        cams = SecondSight.Cameras.CameraManager.getCameras()
        executor = concurrent.futures.ThreadPoolExecutor(max_workers=len(cams))
        futures = {}
        for i, cam in enumerate(cams):
            if cam.hasRole('apriltags'):
                futures[i] = executor.submit(SecondSight.AprilTags.Detector.getPosition, cam.gray, cam.camera_matrix, None)
        for i, future in futures.items():
            dets = future.result()
            if dets:
                for det in dets:
                    det = det.json(error=True)
                    det['camera'] = i
                    res.append(det)
        self.current_apriltags = res

    def getApriltags(self):
        return self.current_apriltags

    def postApriltags(self):
        config = SecondSight.config.Configuration()
        if config.get_value('detects') is not None and "apriltags" in [i[:min(len(i) - 1, 9)] for i in config.get_value('detects')]:
            nt_send = []
            for det in self.current_apriltags:
                det = det.json()
                nt_send += [det['distance'], det['left_right'], det['up_down'], det['pitch'], det['roll'], det['yaw'],
                            det['distance_std'], det['left_right_std'], det['yaw_std'], det['rms'], det['error'],
                            det['tagid'], det['camera']]
            self.april_table.putNumberArray('relative_positions', nt_send)


if __name__ == "main":
    pass
else:
    pass
