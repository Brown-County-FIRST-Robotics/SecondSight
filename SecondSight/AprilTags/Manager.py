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
        self.current_field_pos: tuple[float, float, float] = (-1, -1, -1)
        self.april_table = networktables.NetworkTables.getTable('SecondSight').getSubTable('Apriltags')
        self.fetchApriltags()

    def fetchApriltags(self):
        year: str = ''
        for i in SecondSight.config.Configuration().get_value('detects'):
            if i.startswith('apriltags'):
                year = i.strip('apriltags')
        json_res = []
        res: List[SecondSight.AprilTags.Detector.ApriltagDetection] = []
        cams = SecondSight.Cameras.CameraManager.getCameras()
        executor = concurrent.futures.ThreadPoolExecutor(max_workers=len(cams))
        futures = {}
        for i, cam in enumerate(cams):
            if cam.hasRole('apriltags'):
                futures[i] = executor.submit(SecondSight.AprilTags.Detector.getPosition, cam.gray, cam.camera_matrix, None)
        for i, future in futures.items():
            dets = future.result()
            if dets:
                res += dets
                for det in dets:
                    det = det.json(error=True)
                    det['camera'] = i
                    json_res.append(det)
        self.current_apriltags = json_res
        if len(res) == 1:
            res[0].calcFieldPos(year)
            self.current_field_pos = (res[0].field_x, res[0].field_y, res[0].field_yaw)
        elif len(res) > 1:
            self.current_field_pos = SecondSight.AprilTags.Detector.fuseApriltags(res, year)

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
            self.april_table.putNumber('field_x', self.current_field_pos[0])
            self.april_table.putNumber('field_y', self.current_field_pos[1])
            self.april_table.putNumber('field_ang', self.current_field_pos[2])
