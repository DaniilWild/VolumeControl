# opencv-python
# mediapip
# pycaw

import cv2
import math
import HandTrackingModule111 as HTM
import numpy as np
########################
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
    IAudioEndpointVolume._iid_, CLSCTX_ALL, None)

volume = cast(interface, POINTER(IAudioEndpointVolume))
volRange = volume.GetVolumeRange()

minVol = volRange[0]
maxVol = volRange[1]
print(volRange)

########################



cap = cv2.VideoCapture(0)
cap.set(3, 640)
cap.set(4, 480)

detector = HTM.FindHands()

while True:
    ret, img = cap.read()

    hand1_positions = detector.getPosition(img, range(21), draw=False)
    #hand2_positions = detector.getPosition(img, range(21), hand_no=1, draw=False)


    hand1_positions_new = hand1_positions[4:11:4] #4 8 12
    if len(hand1_positions_new)!=0:
        #print(hand1_positions_new[0][0])
        x1, y1 = hand1_positions_new[0][0], hand1_positions_new[0][1]
        x2, y2 = hand1_positions_new[1][0], hand1_positions_new[1][1]

        cv2.line(img, (x1,y1), (x2,y2), (255,0,255) , thickness = 3)
        cx, cy = (x1 + x2)//2, (y1 + y2)//2
        cv2.circle(img, (cx, cy), 5, (255, 0, 0), cv2.FILLED)

        lenght = math.hypot(x2 - x1, y2 - y1)
        #print(lenght)

        vol =  np.interp(lenght,[40,300] , [minVol, maxVol])

        volBar = np.interp(lenght,[40,300] , [400,150])
        volume.SetMasterVolumeLevel(vol, None)
        print(lenght, vol)

        cv2.rectangle(img , (50, 150), (85,400) , (0,255,0), 3) #RGB
        cv2.rectangle(img, (50 ,int(volBar)), (85, 400), (0, 255, 0), cv2.FILLED)
        if lenght < 40:
            cv2.circle(img, (cx, cy), 5, (255, 255, 0), cv2.FILLED)

    for pos in hand1_positions_new:
        cv2.circle(img, pos, 5, (0,255,0), cv2.FILLED)

    cv2.imshow("Image", img)
    #cv2.waitKey(10)

    if cv2.waitKey(10) == ord('q'):
        break