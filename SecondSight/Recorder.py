import random
import time
from typing import Tuple, List

import ntcore

import SecondSight
import cv2


class RecordingManager:
    instance = None

    @classmethod
    def getInst(cls):
        if cls.instance is None:
            cls.instance = RecordingManager()
        return cls.instance

    def __init__(self):
        self.isRecording = False
        self.rebuild()
        self.lastTime = 0

    def rebuild(self):
        self.stopRecording()
        self.writers = [None for _ in SecondSight.Cameras.CameraManager.getCameras()]
        inst = ntcore.NetworkTableInstance.getDefault()
        rtable = inst.getTable(SecondSight.config.Configuration().get_value('inst_name', 'SS_INST'))
        self.publishers: List[Tuple[ntcore.BooleanPublisher, ntcore.StringPublisher]] = [(rtable.getSubTable(str(i)).getBooleanTopic("isRecording").publish(), rtable.getSubTable(str(i)).getStringTopic("recordingPath").publish()) for i in range(len(SecondSight.Cameras.CameraManager.getCameras()))]
        if self.isRecording:
            self.startRecording()

    def startRecording(self, name: str = SecondSight.utils.get8601date()+str(random.randint(0,100000))):
        if self.isRecording:
            return
        self.isRecording = True
        self.writers = [None for _ in SecondSight.Cameras.CameraManager.getCameras()]
        inst = ntcore.NetworkTableInstance.getDefault()
        rtable = inst.getTable(SecondSight.config.Configuration().get_value('inst_name'))
        self.publishers = [(rtable.getSubTable(str(i)).getBooleanTopic("isRecording").publish(), rtable.getSubTable(str(i)).getStringTopic("recordingPath").publish()) for i in range(len(SecondSight.Cameras.CameraManager.getCameras()))]
        for i, cam in enumerate(SecondSight.Cameras.CameraManager.getCameras()):
            self.writers[i] = cv2.VideoWriter(f'recordings/{name}_{i}.avi', cv2.VideoWriter_fourcc(*'MP42'), 10.0, (int(cam.width), int(cam.height)))
            self.publishers[i][0].set(True)
            self.publishers[i][1].set(f'recordings/{name}_{i}.avi')

    def loop(self):
        if len(self.writers) != len(SecondSight.Cameras.CameraManager.getCameras()):
            self.rebuild()
        if self.isRecording and time.time()-self.lastTime>0.1:
            self.lastTime=time.time()
            for cam, writer in zip(SecondSight.Cameras.CameraManager.getCameras(), self.writers):
                writer.write(cam.frame)

    def stopRecording(self):
        if self.isRecording:
            self.isRecording = False
            for i, writer in enumerate(self.writers):
                self.publishers[i][0].set(False)
                writer.release()
