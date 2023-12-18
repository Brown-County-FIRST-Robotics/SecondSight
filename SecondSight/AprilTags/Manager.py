import time

import SecondSight
import concurrent.futures
from typing import Dict
import ntcore

from SecondSight.utils import LogMe


class ApriltagManager:
    instance = None

    @classmethod
    def getInst(cls):
        if cls.instance is None:
            cls.instance = ApriltagManager()
        return cls.instance

    def __init__(self):
        inst = ntcore.NetworkTableInstance.getDefault()
        self.tables: Dict[int, ntcore.NetworkTable] = {i: inst.getTable(f'SecondSight_{i}') for i in range(len(SecondSight.Cameras.CameraManager.getCameras()))}
        self.fetchApriltags()

    @LogMe
    def fetchApriltags(self):
        cams = SecondSight.Cameras.CameraManager.getCameras()
        executor = concurrent.futures.ThreadPoolExecutor(max_workers=len(cams))
        futures = {}
        for i, cam in enumerate(cams):
            if cam.hasRole('apriltags'):
                futures[i] = executor.submit(SecondSight.AprilTags.Detector.getCoords, cam.gray)
        for i, future in futures.items():
            dets = future.result()
            if len(dets) == -1:
                a = SecondSight.AprilTags.Detector.getRelativePosition(dets[0], SecondSight.Cameras.CameraManager.getCamera(i).camera_matrix, None)
                self.tables[i].putNumber('y', a.y)
                self.tables[i].putNumber('z', a.z)
                self.tables[i].putNumber('x', a.x)
                self.tables[i].putNumber('pitch', a.pitch)
                self.tables[i].putNumber('roll', a.roll)
                self.tables[i].putNumber('yaw', a.yaw)
                self.tables[i].putString('proc', 'Single')
                self.tables[i].putNumber('tagid', a.tagID)
                self.tables[i].putNumber('offset', time.time() - SecondSight.Cameras.CameraManager.getTime(i))
            elif len(dets) >= 1:
                a,b = SecondSight.AprilTags.Detector.getFieldPosition(dets, SecondSight.Cameras.CameraManager.getCamera(i).camera_matrix, None)
                self.tables[i].putNumber('x', a.x)
                self.tables[i].putNumber('z', a.z)
                self.tables[i].putNumber('y', a.y)
                self.tables[i].putNumber('pitch', a.pitch)
                self.tables[i].putNumber('roll', a.roll)
                self.tables[i].putNumber('yaw', a.yaw)
                self.tables[i].putString('proc', 'Multiple')
                self.tables[i].putNumber('offset', time.time() - SecondSight.Cameras.CameraManager.getTime(i))
                self.tables[i].putNumberArray("Pose", [a.x, a.y, a.yaw])
                self.tables[i].putNumberArray("Pose2", [b.x, b.y, b.yaw])
                self.tables[i].putNumberArray("Pose3", [SecondSight.AprilTags.Positions.apriltagFeatures['2023']['1'][-1],SecondSight.AprilTags.Positions.apriltagFeatures['2023']['1'][-3]*-2,0])


