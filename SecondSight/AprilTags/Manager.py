import math
import time

import SecondSight
import concurrent.futures
from typing import Dict, Tuple
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
        rtable = inst.getTable(SecondSight.config.Configuration().get_value('inst_name'))
        pub_config = ntcore.PubSubOptions(periodic=0, sendAll=True, keepDuplicates=True)
        self.publishers: Dict[int, Tuple[ntcore.DoubleArrayPublisher, ntcore.StringArrayPublisher]] = {i: (rtable.getSubTable(str(i)).getDoubleArrayTopic("Poses").publish(pub_config), rtable.getSubTable(str(i)).getStringArrayTopic("IDs").publish(pub_config)) for i in range(len(SecondSight.Cameras.CameraManager.getCameras()))}
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
            if len(dets) > 0:
                poses = []
                ids = []
                for det in dets:
                    pos = SecondSight.AprilTags.Detector.getRelativePosition(det, SecondSight.Cameras.CameraManager.getCamera(i).camera_matrix, None)
                    ids.append(str(pos.tagID))
                    poses += [pos.x, pos.y, pos.z, pos.roll, pos.pitch, pos.yaw]
                self.publishers[i][0].set(poses, math.floor(SecondSight.Cameras.CameraManager.getTime(i) * 1000000))
                self.publishers[i][1].set(ids, math.floor(SecondSight.Cameras.CameraManager.getTime(i) * 1000000))
