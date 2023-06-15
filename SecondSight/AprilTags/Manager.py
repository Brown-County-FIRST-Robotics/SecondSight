import SecondSight
import concurrent.futures
from typing import List
import networktables


class ApriltagManager:
    instance = None

    @classmethod
    def getInst(cls):
        if cls.instance is None:
            cls.instance = ApriltagManager()
        return cls.instance

    def __init__(self):
        self.current_apriltags: List[SecondSight.AprilTags.Detector.ApriltagDetection] = []
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
