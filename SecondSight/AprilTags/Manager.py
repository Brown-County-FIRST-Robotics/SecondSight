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
        rtable = inst.getTable(SecondSight.config.Configuration().get_value('inst_name', 'SS_INST'))
        pub_config = ntcore.PubSubOptions(periodic=0, sendAll=True, keepDuplicates=True)
        self.publishers: Dict[int, Tuple[ntcore.DoubleArrayPublisher, ntcore.StringArrayPublisher,ntcore.DoublePublisher]] = {i: (rtable.getSubTable(str(i)).getDoubleArrayTopic("Pose").publish(pub_config), rtable.getSubTable(str(i)).getStringArrayTopic("IDs").publish(pub_config),rtable.getSubTable(str(i)).getDoubleTopic("RMSError").publish(pub_config)) for i in range(len(SecondSight.Cameras.CameraManager.getCameras()))}
        self.fetchApriltags()

    @LogMe
    def fetchApriltags(self):
        cams = SecondSight.Cameras.CameraManager.getCameras()
        if len(cams) > 0:
            executor = concurrent.futures.ThreadPoolExecutor(max_workers=len(cams))
            futures = {}
            for i, cam in enumerate(cams):
                if cam.hasRole('apriltags'):
                    futures[i] = executor.submit(SecondSight.AprilTags.Detector.getCoords, cam.gray)
            for i, future in futures.items():
                dets = future.result()
                if len(dets) == 1:
                    a = SecondSight.AprilTags.Detector.getRelativePosition(dets[0], SecondSight.Cameras.CameraManager.getCamera(i).camera_matrix, None)
                    self.publishers[i][0].set([a.x,a.y,a.z,a.rotation.w,a.rotation.x,a.rotation.y,a.rotation.z], math.floor(SecondSight.Cameras.CameraManager.getTime(i) * 1000000))
                    self.publishers[i][1].set([str(a.tagID)], math.floor(SecondSight.Cameras.CameraManager.getTime(i) * 1000000))
                    self.publishers[i][2].set(a.rms, math.floor(SecondSight.Cameras.CameraManager.getTime(i) * 1000000))
                elif len(dets) > 1:
                    a = SecondSight.AprilTags.Detector.getFieldPosition(dets, SecondSight.Cameras.CameraManager.getCamera(i).camera_matrix, None)
                    self.publishers[i][0].set([a.x, a.y, a.z, a.rotation.w, a.rotation.x, a.rotation.y, a.rotation.z], math.floor(SecondSight.Cameras.CameraManager.getTime(i) * 1000000))
                    self.publishers[i][1].set([str(det[1]) for det in dets], math.floor(SecondSight.Cameras.CameraManager.getTime(i) * 1000000))
                    self.publishers[i][2].set(a.rms, math.floor(SecondSight.Cameras.CameraManager.getTime(i) * 1000000))
