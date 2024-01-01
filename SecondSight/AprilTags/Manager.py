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
                self.tables[i].putNumber('rw', a.rotation.w)
                self.tables[i].putNumber('rx', a.rotation.x)
                self.tables[i].putNumber('ry', a.rotation.y)
                self.tables[i].putNumber('rz', a.rotation.z)
                self.tables[i].putString('proc', 'Single')
                self.tables[i].putNumber('tagid', a.tagID)
                self.tables[i].putNumber('offset', time.time() - SecondSight.Cameras.CameraManager.getTime(i))
            elif len(dets) >= 1:
                a = SecondSight.AprilTags.Detector.getFieldPosition(dets, SecondSight.Cameras.CameraManager.getCamera(i).camera_matrix, None)
                self.tables[i].putNumber('x', a.x)
                self.tables[i].putNumber('z', a.z)
                self.tables[i].putNumber('y', a.y)
                self.tables[i].putNumber('rw', a.rotation.w)
                self.tables[i].putNumber('rx', a.rotation.x)
                self.tables[i].putNumber('ry', a.rotation.y)
                self.tables[i].putNumber('rz', a.rotation.z)
                self.tables[i].putString('proc', 'Multiple')
                self.tables[i].putNumberArray("Pose", [a.x, a.y,a.z, a.rotation.w, a.rotation.x, a.rotation.y, a.rotation.z])
                # self.tables[i].putNumberArray("Pose3", [SecondSight.AprilTags.Positions.apriltagFeatures['2023']['1'][-1],SecondSight.AprilTags.Positions.apriltagFeatures['2023']['1'][-3]*-1,0])
                # self.tables[i].putNumberArray("Pose4", [0,0,0])



