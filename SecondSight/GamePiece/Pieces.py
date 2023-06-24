import SecondSight
import cv2
import numpy as np
import math


class BaseGamePiece:
    def __init__(self, piece_type: str, x: float, y: float, width: float, height: float, theta: float):
        self.piece_type = piece_type
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.theta = theta
        self.pitch = None
        self.yaw = None
        self.roll = None
        self.left_right = None
        self.distance = None
        self.up_down = None
        self.rms = None

    def computePose(self, camera_matrix, dist):
        box = cv2.boxPoints(((self.x, self.y), (self.width, self.height), self.theta))
        image_points = np.array(box).reshape(1, 4, 2)

        good, rotation_vector, translation_vector, self.rms = cv2.solvePnPGeneric(SecondSight.GamePiece.PieceConstants.PTS[self.piece_type], image_points,
                                                                                  camera_matrix,
                                                                                  dist,
                                                                                  flags=cv2.SOLVEPNP_ITERATIVE)
        assert good, 'something went wrong with solvePnP'

        self.pitch, self.yaw, self.roll = [float(i) for i in rotation_vector[0] * 180 / math.pi]

        self.left_right = translation_vector[0][0]
        self.up_down = translation_vector[0][1]
        self.distance = translation_vector[0][2]

    def jsonify(self, error=False):
        res = {
            'pitch': self.pitch,
            'yaw': self.yaw,
            'roll': self.roll,
            'left_right': self.left_right,
            'up_down': self.up_down,
            'distance': self.distance,
            'type': self.piece_type
        }
        if error:
            res['rms'] = self.rms
        return res

    def draw(self, frame, color: tuple[int, int, int], thickness: int = 2):  # TODO: test
        box = cv2.boxPoints((self.x, self.y), (self.width, self.height), self.theta)
        box = np.int0(box)
        return cv2.drawContours(frame, [box], 0, color, thickness)


class Cube2023(BaseGamePiece):
    def __init__(self, x: float, y: float, width: float, height: float, theta: float):
        super().__init__('cube2023', x, y, width, height, theta)


class Cone2023(BaseGamePiece):
    def __init__(self, x: float, y: float, width: float, height: float, theta: float):
        super().__init__('cone2023', x, y, width, height, theta)
