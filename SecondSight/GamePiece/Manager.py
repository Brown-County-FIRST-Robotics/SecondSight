import SecondSight
import networktables
import concurrent.futures
from typing import List, Tuple


class GamePieceManager:
    inst = None

    @classmethod
    def getInst(cls):
        if cls.inst is None:
            cls.inst = GamePieceManager()
        return cls.inst

    def __init__(self):
        self.pieces: List[Tuple[SecondSight.GamePiece.Pieces.BaseGamePiece, int]] = []
        self.gamepiece_table: networktables.NetworkTable = networktables.NetworkTables.getTable('SecondSight').getSubTable('GamePieces')

    def fetchPieces(self):
        cams = SecondSight.Cameras.CameraManager.getCameras()
        executor = concurrent.futures.ThreadPoolExecutor(max_workers=len(cams) * 2)
        conf = SecondSight.config.Configuration()
        futures = []
        for obj in conf.get_value('detects'):
            if obj in ['cube2023', 'cone2023']:
                for i, cam in enumerate(cams):
                    if cam.hasRole('conecube'):
                        futures.append((executor.submit(SecondSight.GamePiece.Detector.findGivenPieceType, cam.frame, obj), i))
        res: List[Tuple[SecondSight.GamePiece.Pieces.BaseGamePiece, int]] = []
        for future, i in futures:
            dets = future.result()
            for det in dets:
                det.computePose(cams[i].camera_matrix, None)
                res.append((det, i))
        self.pieces = res
