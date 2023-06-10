#!/usr/bin/env python

# mostly coppied from https://github.com/kyle-bersani/opencv-examples/blob/master/CalibrationByCharucoBoard/CalibrateCamera.py
# with a little from https://mecaruco2.readthedocs.io/en/latest/notebooks_rst/Aruco/sandbox/ludovic/aruco_calibration_rotation.html

import sys
import numpy
import cv2
import json
import glob, time

import SecondSight.Cameras


def makeArucoDict():
    CHARUCOBOARD_ROWCOUNT = 7
    CHARUCOBOARD_COLCOUNT = 5
    ARUCO_DICT = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_5X5_1000)

    # Create constants to be passed into OpenCV and Aruco methods
    CHARUCO_BOARD = cv2.aruco.CharucoBoard((5, 7), 0.04, 0.02, ARUCO_DICT, None)
    return ARUCO_DICT, CHARUCO_BOARD


def makeImage():
    ARUCO_DICT, CHARUCO_BOARD = makeArucoDict()
    imboard = CHARUCO_BOARD.generateImage((2000, 2000))
    cv2.imwrite("SecondSight/webserver/static/charuco.tiff", imboard)
    print('charuco file written')


def genCalibrationFrames(ind: int, min_captures: int = 30):
    cam=SecondSight.Cameras.CameraManager.getCamera(ind)
    img_counter = 0
    corners_all = []
    ids_all = []
    ARUCO_DICT, CHARUCO_BOARD = makeArucoDict()
    captures = 0
    frames_until_capture = 5
    last_frame_time = 0
    while captures < min_captures:
        while time.time() < last_frame_time + 0.1:
            time.sleep(0.001)
        frame = cam.uncalibrated.copy()

        if frames_until_capture == 0:
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            image_size = gray.shape[::-1]

            # Find aruco markers in the query image
            corners, ids, _ = cv2.aruco.detectMarkers(image=gray, dictionary=ARUCO_DICT)

            # Outline the aruco markers found in our query image
            frame = cv2.aruco.drawDetectedMarkers(image=frame, corners=corners)

            # Get charuco corners and ids from detected aruco markers
            try:
                response, charuco_corners, charuco_ids = cv2.aruco.interpolateCornersCharuco(
                    markerCorners=corners,
                    markerIds=ids,
                    image=gray,
                    board=CHARUCO_BOARD)

                frame = cv2.aruco.drawDetectedCornersCharuco(
                    image=frame,
                    charucoCorners=charuco_corners,
                    charucoIds=charuco_ids)
            except:
                response = 0
                # Draw the Charuco board we've detected to show our calibrator the board was properly detected

            if response > 20:
                # Add these corners and ids to our calibration arrays
                corners_all.append(charuco_corners)
                ids_all.append(charuco_ids)
                captures += 1
            else:
                cv2.putText(frame, 'Charuco not found', (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (20, 20, 255), 2,
                            cv2.LINE_AA)
            frames_until_capture = 5
        cv2.putText(frame, f'{str(100*captures/min_captures)[:3].strip(".")}%', (cam.width-120,cam.height-60), cv2.FONT_HERSHEY_SIMPLEX, 1, (20, 255, 0), 2,
                    cv2.LINE_AA)
        ret, buffer = cv2.imencode('.jpg', frame)
        img_bytes = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + img_bytes + b'\r\n')
        frames_until_capture -= 1
        last_frame_time = time.time()
    frame = cam.uncalibrated.copy()
    cv2.putText(frame, 'Processing images', (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (20, 255, 20), 2,
                cv2.LINE_AA)
    ret, buffer = cv2.imencode('.jpg', frame)
    img_bytes = buffer.tobytes()
    yield (b'--frame\r\n'
           b'Content-Type: image/jpeg\r\n\r\n' + img_bytes + b'\r\n')

    # Now that we've seen all of our images, perform the camera calibration
    # based on the set of points we've discovered
    calibration, cameraMatrix, distCoeffs, rvecs, tvecs = cv2.aruco.calibrateCameraCharuco(
            charucoCorners=corners_all,
            charucoIds=ids_all,
            board=CHARUCO_BOARD,
            imageSize=image_size,
            cameraMatrix=None,
            distCoeffs=None)
    frame = cam.uncalibrated.copy()
    cv2.putText(frame, 'Calibration complete', (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (20, 255, 20), 2,
                cv2.LINE_AA)
    ret, buffer = cv2.imencode('.jpg', frame)
    img_bytes = buffer.tobytes()
    yield (b'--frame\r\n'
           b'Content-Type: image/jpeg\r\n\r\n' + img_bytes + b'\r\n')

    # Print matrix and distortion coefficient to the console
    out = [cameraMatrix.tolist(), distCoeffs.tolist()]
    print(out)
