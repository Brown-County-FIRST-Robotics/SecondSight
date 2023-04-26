#!/usr/bin/env python


#mostly coppied from https://github.com/kyle-bersani/opencv-examples/blob/master/CalibrationByCharucoBoard/CalibrateCamera.py
#with a little from https://mecaruco2.readthedocs.io/en/latest/notebooks_rst/Aruco/sandbox/ludovic/aruco_calibration_rotation.html

import sys
import numpy
import cv2
import json
import glob

def main():
    # ChAruco board variables
    ARUCO_DICT = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_5X5_1000)

    # Create constants to be passed into OpenCV and Aruco methods
    #CHARUCO_BOARD = cv2.aruco.CharucoBoard(1,
    #        squaresX=CHARUCOBOARD_COLCOUNT,
    #        squaresY=CHARUCOBOARD_ROWCOUNT,
    #        squareLength=0.029,
    #        markerLength=0.014,
    #        dictionary=ARUCO_DICT)


    paper_size = (20,30) #inches
    min_square_size = 2 #inches
    num_squares = [(s-2)//min_square_size for s in paper_size] #leave a border row of one inch around edge
    square_size=[(paper_size[i]-2)/num_squares[i] for i in range(2)] #inches
    size = min(square_size)

    ppi=11 * 10 #found by hand to be minimum (11) for the 20,30.  you should try other values to not have the blur

    CHARUCO_BOARD = cv2.aruco.CharucoBoard(num_squares, size, size*.6, ARUCO_DICT, None)
    #print(CHARUCO_BOARD.getChessboardCorners())

    if 'generate' in sys.argv[1:]:
        imboard=CHARUCO_BOARD.generateImage((ppi*(num_squares[0]+2), ppi*(num_squares[1]+2)), None, ppi)
        cv2.imwrite("chessboard.tiff", imboard)
        print('chessboard.tiff written')
        sys.exit()


    # Create the arrays and variables we'll use to store info like corners and IDs from images processed
    corners_all = [] # Corners discovered in all images processed
    ids_all = [] # Aruco ids corresponding to corners discovered
    image_size = None # Determined at runtime


    camnum = 0
    cam = cv2.VideoCapture(camnum)

    #cam.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
    #cam.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)

    cam.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cam.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

    video_size = (cam.get(cv2.CAP_PROP_FRAME_WIDTH), cam.get(cv2.CAP_PROP_FRAME_HEIGHT))
    as_int = tuple(int(x) for x in video_size)
    assert as_int == video_size
    video_size = as_int
    print('size', video_size)

    cv2.namedWindow("test")

    img_counter = 0
    corners_all = []
    ids_all = []

    while True:
        ret, img = cam.read()
        if not ret:
            print("failed to grab img")
            break

        dispimg = img.copy()
        proportion = max(dispimg.shape) / 1000.0
        dispimg = cv2.resize(dispimg, (int(dispimg.shape[1] / proportion), int(dispimg.shape[0] / proportion)))
        cv2.putText(dispimg, 'press space to capture', (50,200), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,0,0), 2, cv2.LINE_AA)

        cv2.imshow("test", dispimg)

        # Grayscale the image
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        image_size = gray.shape[::-1]

        # Find aruco markers in the query image
        corners, ids, _ = cv2.aruco.detectMarkers(image=gray, dictionary=ARUCO_DICT)

        # Outline the aruco markers found in our query image
        img = cv2.aruco.drawDetectedMarkers(image=img, corners=corners)

        # Get charuco corners and ids from detected aruco markers
        try:
            response, charuco_corners, charuco_ids = cv2.aruco.interpolateCornersCharuco(
                markerCorners=corners,
                markerIds=ids,
                image=gray,
                board=CHARUCO_BOARD)

            img = cv2.aruco.drawDetectedCornersCharuco(
                image=img,
                charucoCorners=charuco_corners,
                charucoIds=charuco_ids)

        except:
            response = 0
            # Draw the Charuco board we've detected to show our calibrator the board was properly detected

        proportion = max(img.shape) / 1000.0
        img = cv2.resize(img, (int(img.shape[1] / proportion), int(img.shape[0] / proportion)))

        if response > 20:
            #Add these corners and ids to our calibration arrays
            corners_all.append(charuco_corners)
            ids_all.append(charuco_ids)
            img_counter += 1
        else:
            cv2.putText(img, 'Charuco not found', (50,50), cv2.FONT_HERSHEY_SIMPLEX, 1, (20,20,255), 2, cv2.LINE_AA)

        cv2.putText(img, 'press space to continue', (50,200), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,0,0), 2, cv2.LINE_AA)

        cv2.imshow("test", img)
        k = cv2.waitKey(1)
        if k % 256 == 27:
            # ESC pressed
            print("Escape hit, breaking loop...")
            break



        print("Captured image %d" % img_counter)

    cam.release()

    cv2.destroyAllWindows()

    # Make sure at least one image was found
    if img_counter < 5:
        # Calibration failed because there were not enough images, warn the user
        print("Calibration was unsuccessful. Need at least 5 images.")
        # Exit for failure
        exit()


    # Now that we've seen all of our images, perform the camera calibration
    # based on the set of points we've discovered
    calibration, cameraMatrix, distCoeffs, rvecs, tvecs = cv2.aruco.calibrateCameraCharuco(
            charucoCorners=corners_all,
            charucoIds=ids_all,
            board=CHARUCO_BOARD,
            imageSize=image_size,
            cameraMatrix=None,
            distCoeffs=None)

    # Print matrix and distortion coefficient to the console
    out = [cameraMatrix.tolist(), distCoeffs.tolist()]
    print(out)
