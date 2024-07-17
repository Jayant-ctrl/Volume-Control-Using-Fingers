import cv2
import time
import numpy as np
import HandTrackingModule as htm
import math
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
##################################
wCam, hCam = 640, 480
##################################

capture = cv2.VideoCapture(0)
capture.set(3, wCam)
capture.set(4, hCam)
pTime = 0

detector = htm.handDetector(detectionCon = 0.7)


devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
    IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = interface.QueryInterface(IAudioEndpointVolume)
#volume.GetMute()
#volume.GetMasterVolumeLevel()
volRange = volume.GetVolumeRange()


minVol = volRange[0]
maxVol = volRange[1]

vol = 0
volBar = 400
volPer = 0
while True:
    isTrue, frame = capture.read()
    frame = detector.findHands(frame)
    lmList = detector.findPosition(frame, draw = False)
    
    if len(lmList) != 0:       
     #print(lmList[4], lmList[8])
    
     x1, y1 = lmList[4][1], lmList[4][2]
     x2, y2 = lmList[8][1], lmList[8][2]
     cx, cy = (x1+x2)//2, (y1+y2)//2
     
     cv2.circle(frame, (x1, y1), 15, (255,0,255), -1)
     cv2.circle(frame, (x2, y2), 15, (255,0,255), -1)
     cv2.line(frame, (x1, y1), (x2, y2), (255,0,255), 3)
     cv2.circle(frame, (cx, cy), 15, (255,0,255), -1)

     length = math.hypot(x2-x1, y2-y1)
     #print(length)
     
     vol = np.interp(length, [23, 280], [minVol, maxVol])
     volBar = np.interp(length, [23, 280], [400, 150])
     volPer = np.interp(length, [23, 280], [0, 100])
     print(int(length), vol)
     volume.SetMasterVolumeLevel(vol, None)

     if length<32:
        cv2.circle(frame, (cx, cy), 15, (0,0,255), -1)
    
    cv2.rectangle(frame, (50, 150), (85,400), (255,0,0), 3)
    cv2.rectangle(frame, (50, int(volBar)), (85,400), (255,0,0), -1)
    cv2.putText(frame, f'{int(volPer)}%', (40, 450), cv2.FONT_HERSHEY_COMPLEX, 1, (255,0,0), 2)
    
    cTime = time.time()
    fps = 1/(cTime-pTime)
    pTime = cTime
   
    cv2.putText(frame, f'FPS: {int(fps)}', (40, 50), cv2.FONT_HERSHEY_COMPLEX, 1, (255,0,0), 2)

    cv2.imshow('video',frame)
    cv2.waitKey(1)

    
