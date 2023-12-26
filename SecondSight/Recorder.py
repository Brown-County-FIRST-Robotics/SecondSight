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
        self.writers = [None for _ in SecondSight.Cameras.CameraManager.getCameras()]
        self.isRecording = False
        inst = ntcore.NetworkTableInstance.getDefault()
        rtable = inst.getTable(SecondSight.config.Configuration().get_value('inst_name'))
        self.publishers: List[Tuple[ntcore.BooleanPublisher, ntcore.StringPublisher]] = [(rtable.getSubTable(str(i)).getBooleanTopic("isRecording").publish(), rtable.getSubTable(str(i)).getStringTopic("recordingPath").publish()) for i in range(len(SecondSight.Cameras.CameraManager.getCameras()))]

    def startRecording(self, name: str = SecondSight.utils.get8601date()):
        if self.isRecording:
            return
        for i, cam in enumerate(SecondSight.Cameras.CameraManager.getCameras()):
            self.writers[i] = cv2.VideoWriter(f'{name}_{i}.avi', cv2.VideoWriter_fourcc(*'MP42'), 15.0, (cam.width, cam.height))
            self.publishers[i][0].set(True)
            self.publishers[i][1].set(f'{name}_{i}.avi')

    def loop(self):
        while self.isRecording:
            for cam, writer in zip(SecondSight.Cameras.CameraManager.getCameras(), self.writers):
                writer.write(cam.read())
