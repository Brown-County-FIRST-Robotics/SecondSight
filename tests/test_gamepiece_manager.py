import math
import unittest
import tempfile
import SecondSight
import networktables
import random
import tests.make_apriltag_cases

import cv2
import os
import json
import time
import numpy as np


class TestGamePieceManager(unittest.TestCase):
    def setUp(self) -> None:
        networktables.NetworkTables.initialize(server='localhost')
        self.manager = SecondSight.GamePiece.Manager.GamePieceManager.getInst()
        self.manager.pieces = [(SecondSight.GamePiece.Pieces.Cone2023(1, 1, 1, 1, 1), 0),
                               (SecondSight.GamePiece.Pieces.Cube2023(1, 1, 1, 1, 1), 0)
                               ]

    def testSingleton(self):
        self.assertIs(SecondSight.GamePiece.Manager.GamePieceManager.getInst(), self.manager, "The getInst() method does not work; it returned the wrong object")

    def testGetPieces(self):
        self.assertEqual(self.manager.pieces, self.manager.getPieces())
