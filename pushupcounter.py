import cv2 
import cvzone
from cvzone.PoseModule import PoseDetector
import math
import time
import numpy as np 

cam = cv2.VideoCapture(0)

Detector = PoseDetector()


def findAngle(img, p1, p2, p3, lmList, draw=True):
        """
        Finds angle between three points. Inputs index values of landmarks
        instead of the actual points.
        :param img: Image to draw output on.
        :param p1: Point1 - Index of Landmark 1.
        :param p2: Point2 - Index of Landmark 2.
        :param p3: Point3 - Index of Landmark 3.
        :param draw:  Flag to draw the output on the image.
        :return:
        """

        # Get the landmarks
        x1, y1 = lmList[p1][1], lmList[p1][2]
        x2, y2 = lmList[p2][1], lmList[p2][2]
        x3, y3 = lmList[p3][1], lmList[p3][2]

        # Calculate the Angle
        angle = math.degrees(math.atan2(y3 - y2, x3 - x2) -
                             math.atan2(y1 - y2, x1 - x2))
        if angle < 0:
            angle += 360

        # Draw
        if draw:
            cv2.line(img, (x1, y1), (x2, y2), (255, 255, 255), 3)
            cv2.line(img, (x3, y3), (x2, y2), (255, 255, 255), 3)
            cv2.circle(img, (x1, y1), 10, (0, 0, 255), cv2.FILLED)
            cv2.circle(img, (x1, y1), 15, (0, 0, 255), 2)
            cv2.circle(img, (x2, y2), 10, (0, 0, 255), cv2.FILLED)
            cv2.circle(img, (x2, y2), 15, (0, 0, 255), 2)
            cv2.circle(img, (x3, y3), 10, (0, 0, 255), cv2.FILLED)
            cv2.circle(img, (x3, y3), 15, (0, 0, 255), 2)
            cv2.putText(img, str(int(angle)), (x2 - 50, y2 + 50),
                        cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 255), 2)
        return angle

dir = 0
pushup = 0


while(True):
    ret, frame = cam.read()
    frame = Detector.findPose(frame, draw=True)
    lmlist, boundarybox = Detector.findPosition(frame, draw=False)
    if(lmlist):
        rangle = findAngle(frame, 12,14,16, lmlist)
        langle = findAngle(frame, 15,13,11, lmlist)
        
        # print("Righ t Angle : ",rangle," Left angle: ",langle)
        per_vall = int(np.interp(langle, (80,160), (100, 0)))
        per_valr = int(np.interp(rangle, (80,160), (100, 0)))
        print(f'left percentage = {per_vall} and right percentage = {per_valr}')
        cvzone.putTextRect(frame, f'l percentage = {per_vall} and r percentage = {per_valr}', pos=(20,20), scale=0.5, thickness=1,colorR=(0,0,0), font=cv2.LINE_AA)
        # print(lmlist[0])
        if(dir == 0):
            if( per_valr==100 or per_vall==100 ):
                pushup+=0.5
                dir = 1
        elif(dir == 1):
            if( per_valr==0 or per_vall==0 ):
                pushup+=0.5
                dir = 0
        
        if(int(pushup) == float(pushup)):
            cvzone.putTextRect(frame, f"PUSH-UP :  {pushup}" , pos = (100,100))
    cv2.imshow('Camera-window', frame)
    if(cv2.waitKey(1) == ord('q')):
        break
