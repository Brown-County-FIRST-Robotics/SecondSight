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
        executor = concurrent.futures.ThreadPoolExecutor(max_workers=len(cams) * len(SecondSight.GamePiece.PieceConstants.PTS))
        conf = SecondSight.config.Configuration()
        futures = []
        for obj in conf.get_value('detects'):
            if obj in SecondSight.GamePiece.PieceConstants.PIECE_NAMES:
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

    def postPieces(self):
        res = {}
        conf = SecondSight.config.Configuration()

        for obj in conf.get_value('detects'):
            if obj in SecondSight.GamePiece.PieceConstants.PIECE_NAMES:
                res[obj] = []
                for det, camnum in self.pieces:
                    res[obj] += [det.distance, det.left_right, det.up_down, det.pitch, det.roll, det.yaw, det.rms, camnum]
                self.gamepiece_table.putNumberArray(obj, res[obj])

    def getPieces(self):
        return self.pieces

    def getSinglePieceJson(self, piece_type: str):
        res = []
        for piece, camnum in self.pieces:
            if piece.piece_type == piece_type:
                res.append({
                    'distance': piece.distance,
                    'left_right': piece.left_right,
                    'up_down': piece.up_down,
                    'pitch': piece.pitch,
                    'yaw': piece.yaw,
                    'roll': piece.roll,
                    'rms': piece.rms,
                    'cam': camnum
                })