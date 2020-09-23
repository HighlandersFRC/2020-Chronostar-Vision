import libjevois as jevois
import cv2
import numpy as np
import json
import math


class HoughTapeDetect:
# ###################################################################################################
## Constructor


    def __init__(self):
        # Instantiate a JeVois Timer to measure our processing framerate:
        self.timer = jevois.Timer("processing timer", 100, jevois.LOG_INFO)
        
        self.draw = True
        
        self.lowerH = 57
        self.upperH = 84
        
        self.lowerS = 222
        self.upperS = 255
        
        self.lowerV = 62
        self.upperV = 255
        
        #gain = 20
        #exposure = 27
        
        self.stringForHSV = "hi"
                
    # ###################################################################################################
    ## Process function with USB output
    def process(self, inframe, outframe):
        #out = self.UniversalProcess(inframe)
        #outframe.sendCv(out)
        #jevois.sendSerial("hello")
        out = self.UniversalProcess(inframe)
        outframe.sendCv(out)

    def processNoUSB(self, inframe):
        out = self.UniversalProcess(inframe)
        #outframe.sendCv(out)
        #jevois.sendSerial("bonjour")
        
    def parseSerial(self, string):
        self.stringForHSV = string
        #jevois.sendSerial("hello parseSerial")
        #jevois.sendSerial(stringForHSV)
        return self.stringForHSV;
    #stringForHSV = string    

    def UniversalProcess(self, inframe):
        inimg = inframe.getCvBGR()
        outimg = inimg
        
        #change to hsv
        hsv = cv2.cvtColor(inimg, cv2.COLOR_BGR2HSV)
        
        arrayForHSV = list(self.stringForHSV)
        
        #threshold colors to detect - Green: First value decides color, second val determines intensity, third val decides brightness
        lowerThreshold = np.array([self.lowerH, self.lowerS, self.lowerV])
        upperThreshold = np.array([self.upperH, self.upperS, self.upperV])
        
        
        if len(arrayForHSV) > 15 and arrayForHSV[4] == "h":
            stringForH = self.stringForHSV.lstrip("set hrange")
            stringHSpace= stringForH.replace("..."," ")
            stringH = stringHSpace.split(" ")
            self.lowerH = int(stringH[0])
            self.upperH = int(stringH[1])
            lowerThreshold = np.array([self.lowerH, self.lowerS, self.lowerV])
            upperThreshold = np.array([self.upperH, self.upperS, self.upperV])
            #jevois.sendSerial("hello")
        if len(arrayForHSV) > 15 and arrayForHSV[4] == "s":
            stringForS = self.stringForHSV.lstrip("set srange")
            stringSSpace= stringForS.replace("..."," ")
            stringS = stringSSpace.split(" ")
            self.lowerS = int(stringS[0])
            self.upperS = int(stringS[1])
            lowerThreshold = np.array([self.lowerH, self.lowerS, self.lowerV])
            upperThreshold = np.array([self.upperH, self.upperS, self.upperV])
        if len(arrayForHSV) > 15 and arrayForHSV[4] == "v":
            stringForV = self.stringForHSV.lstrip("set vrange")
            stringVSpace= stringForV.replace("..."," ")
            stringV = stringVSpace.split(" ")
            self.lowerV = int(stringV[0])
            self.upperV = int(stringV[1])
            lowerThreshold = np.array([self.lowerH, self.lowerS, self.lowerV])
            upperThreshold = np.array([self.upperH, self.upperS, self.upperV])
        #jevois.sendSerial(str(lowerThreshold))
        #jevois.sendSerial(str(upperThreshold))

        #check if color in range
        mask = cv2.inRange(hsv, lowerThreshold, upperThreshold)
        
        result = cv2.bitwise_and(inimg, inimg, mask = mask)
        
        edges = cv2.Canny(mask, 75, 150)
        
        lines = cv2.HoughLinesP(edges,1,np.pi/180,10)
        
        #jevois.sendSerial(str(lines))
        
        numLines = 0
        centerX = 0
        centerY = 0
        
        if lines is not None:
            for i in range(0, len(lines)):
                l = lines[i][0]
                cv2.line(outimg, (l[0], l[1]), (l[2], l[3]), (0, 0, 255), 1, cv2.LINE_AA)
                numLines = numLines + 2
                centerX = centerX + l[0] + l[2]
                centerY = centerY + l[1] + l[3]
        else:
            jevois.sendSerial('{"Distance":-11, "Angle":-100}')
            return outimg
            
        if numLines != 0:
            centerX = centerX/numLines
            centerY = centerY/numLines
            centerY = centerY - 20
            
        centerX = int(centerX)
        centerY = int(centerY)
        
        yawAngle = (centerX - 159.5) * 0.203125
        yawAngle = str(yawAngle)
        distance = "-11"
        
        cv2.circle(outimg, (centerX, centerY), 5, (120, 255, 255))
        
        JSON = '{"Distance":' + distance + ', "Angle":' + yawAngle + '}'
        
        #jevois.sendSerial("CenterX:" + str(centerX))
        #jevois.sendSerial("CenterY:" + str(centerY))
        jevois.sendSerial(JSON)
        
        
        #jevois.sendSerial("hello")
        
        return outimg
        #return outimg