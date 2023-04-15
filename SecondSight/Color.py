#!/usr/bin/env python

import logging
import numpy as np
import cv2
import os
import SecondSight.config

#use this for calibrating the color detector
#pass in frame
#pass in range from center of image that you want to sample
#returns average color is an array
def averageColor(frame, sampleRange):
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    height = len(hsv)
    width = len(hsv[0])
    x = int(width / 2) - sampleRange
    y = int(height / 2) - sampleRange
    hSum = 0
    sSum = 0
    vSum = 0
    for i in range(x, x + 2 * sampleRange):
        for j in range(y, y + 2 * sampleRange):
            hSum += hsv[j][i][0]
            sSum += hsv[j][i][1]
            vSum += hsv[j][i][2]
    averageColor = [ hSum / (4 * sampleRange * sampleRange), sSum / (4 * sampleRange * sampleRange), vSum / (4 * sampleRange * sampleRange) ]
    return averageColor

#GamePiece - can represent a cone or a cube
class GamePiece():
    # position of cone in the image in terms of pixels
    x = 0 #use this for decision
    y = 0 #use this for decision
    #dimensions of bounding rectangle
    w = 0
    h = 0
    imgX = 0 #image coordinates
    imgY = 0 #image coordinates
    # is the cone upright?
    upright = False #Do not care about this value if this is a cube
    lower_color = np.array([ 0, 0, 0 ], np.uint8)
    upper_color = np.array([ 0xFF, 0xFF, 0xFF ], np.uint8)
    notfound = False
    minRatio = -1.0
    maxRatio = 9999999.0

    def setMinRatio(self, ratio):
        self.minRatio = ratio
    def setMaxRatio(self, ratio):
        self.maxRatio = ratio

    def setLowerColor(self, lower):
        self.lower_color = lower
        for i in range(len(self.lower_color)):
            if self.lower_color[i] < 0:
                self.lower_color[i] = 0
            if self.lower_color[i] > 255:
                self.lower_color[i] = 255

    def setUpperColor(self, upper):
        self.upper_color = upper
        for i in range(len(self.upper_color)):
            if self.upper_color[i] < 0:
                self.upper_color[i] = 0
            if self.upper_color[i] > 255:
                self.upper_color[i] = 255

    def getLowerColor(self):
        return self.lower_color

    def getUpperColor(self):
        return self.upper_color

    def isUpright(self):
        return self.upright

    def setUpright(self, up):
        self.upright = up

    def setX(self, xpos):
        self.x = xpos

    def setY(self, ypos):
        self.y = ypos

    def getX(self):
        return self.x
    
    def getY(self):
        return self.y

    def getWidth(self):
        return self.w

    def setWidth(self, width):
        self.w = width

    def getHeight(self):
        return self.h

    def setHeight(self, height):
        self.h = height

    def getNotFound(self):
        return self.notfound
    
    def setNotFound(self, isNotFound):
        self.notfound = isNotFound

    # Returns a cone object when it attempts to find a
    # cone in an image (frame)
    # also passes in the lower color of the cone and upper color of the cone
    def findObject(self, frame):
        logging.info("looking for cone")
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    
        objectMask = cv2.inRange(hsv, self.lower_color, self.upper_color)
          
        res = cv2.bitwise_and(frame, frame, mask=objectMask)

        gray = cv2.cvtColor(res, cv2.COLOR_BGR2GRAY)
    
        contours, hierarchy = cv2.findContours(gray, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE) 
    
        largestBoundRectArea = -1
        lx = ly = lw = lh = 0

        if len(contours) == 0:
            self.notfound = True
            return
        self.notfound = False

        #find largest contour
        for cont in contours:
            x,y,w,h = cv2.boundingRect(cont)
            area = w * h
            if w / h < self.minRatio or w / h > self.maxRatio:
                continue
            if area > largestBoundRectArea:
                largestBoundRectArea = area
                lx = x
                ly = y
                lw = w
                lh = h
       
        """
        # Determine if the cone is upright
        upright = False
        #check if the rectangle's dimensions are in
        if(lw < lh):
            yellowTop = 0
            yellowBot = 0
            for x in range(int(lx), int(lx + lw)):
                for y in range(int(ly), int(ly + lh / 2)):
                    if maskKone[y][x]:
                        yellowTop += 1
            for x in range(int(lx), int(lx + lw)):
                for y in range(int(ly + lh / 2), int(ly + lh)):
                    if maskKone[y][x]:
                        yellowBot += 1
            if yellowTop < yellowBot: 
                upright = True
        """

        frameDimensions = frame.shape
        self.imgX = int(lx + lw / 2)
        self.imgY = int(ly + lh / 2)
        self.setX(int(lx + lw / 2) - int(frameDimensions[1] / 2))
        self.setY(int(ly + lh / 2) - int(frameDimensions[0] / 2))
        self.setHeight(int(lh))
        self.setWidth(int(lw)) 

    def drawBoundRect(self, frame, color):
        return cv2.rectangle(frame, (int(self.imgX - self.w / 2), int(self.imgY - self.h / 2)), (int(self.imgX + self.w / 2), int(self.imgY + self.h / 2)), color, 4, cv2.LINE_AA)

    #green if frame
    def drawCone(self, frame):
        if self.isUpright():
            cv2.rectangle(frame, (int(self.imgX - self.w / 2), int(self.imgY - self.h / 2)), (int(self.imgX + self.w / 2), int(self.imgY + self.h / 2)), [0,255,0], 4, cv2.LINE_AA)
        else:
            cv2.rectangle(frame, (int(self.imgX - self.w / 2), int(self.imgY - self.h / 2)), (int(self.imgX + self.w / 2), int(self.imgY + self.h / 2)), [0,0,255], 4, cv2.LINE_AA)

    def getLowerLeft(self):
        return (int(self.imgX - self.getWidth() / 2), int(self.imgY - self.getHeight() / 2))

    def getUpperRight(self):
        return (int(self.imgX + self.getWidth() / 2), int(self.imgY + self.getHeight() / 2))

    def findCone(self, frame):
        self.findObject(frame)

    def findCube(self, frame):
        self.findObject(frame)

#Color picker
# This function gets called by the /video_feed route below
def gen_preview_picker(camera):  # generate frame by frame from camera
    logging.debug("Vision.gen_frames_picker")

    config = SecondSight.config.Configuration()

    col = config.get_value("cube_hsv")

    cube = GamePiece()

    lower = [col[0] - 5, col[1] - 100, col[2] - 100]
    upper = [col[0] + 5, col[1] + 100, col[2] + 100]

    for i in range(len(lower)):
        if lower[i] < 0:
            lower[i] = 0
        if lower[i] > 255:
            lower[i] = 255

        if upper[i] < 0:
            upper[i] = 0
        if upper[i] > 255:
            upper[i] = 255

    cube.setLowerColor(np.array(lower, dtype=np.uint8))
    cube.setUpperColor(np.array(upper, dtype=np.uint8)) 
    cube.setMinRatio(3.0 / 5.0)
    cube.setMaxRatio(5.0 / 3.0)

    currentFrame = 0

    # We want to loop this forever
    while True:
        frame = camera.get_frame()
       
#        if camera.frame_count == currentFrame:
#            continue     
#        currentFrame = camera.frame_count

        cube.findObject(frame)  
        
        cv2.rectangle(frame, cube.getLowerLeft(), cube.getUpperRight(), (255, 0, 0), 2)
        ret, jpeg = cv2.imencode('.jpg', frame)
        data = jpeg.tobytes()

        # Return the image to the browser
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + data + b'\r\n')  # concat frame one by one and show result

if __name__ == "__main__":
    pass