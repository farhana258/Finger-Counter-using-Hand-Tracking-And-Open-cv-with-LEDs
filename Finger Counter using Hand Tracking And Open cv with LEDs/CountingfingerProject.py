import cv2
import time
import handTrackingModule as htm
import serial

bluetooth_device = 'COM15'
baud_rate = 9600
ser = serial.Serial(bluetooth_device, baud_rate)


def getNumber(ar):
    s = ""
    for i in ar:
        s += str(ar[i]);

    if (s == "00000"):
        ser.write(b'zero')
        return (0)
    elif (s == "01000"):
        ser.write(b'one')
        return (1)
    elif (s == "01100"):
        ser.write(b'two')
        return (2)
    elif (s == "01110"):
        ser.write(b'three')
        return (3)
    elif (s == "01111"):
        ser.write(b'four')
        return (4)
    elif (s == "11111"):
        ser.write(b'five')
        return (5)
    elif (s == "01001"):
        # ser.write(b'seven')
        return (6)
    elif (s == "01011"):
        # ser.write(b'eight')
        return (7)


wcam, hcam = 640, 480
cap = cv2.VideoCapture(0)
cap.set(3, wcam)
cap.set(4, hcam)
pTime = 0
detector = htm.handDetector(detectionCon=0.75)
while True:
    success, img = cap.read()
    img = detector.findHands(img, draw=True)
    lmList = detector.findPosition(img, draw=False)
    # print(lmList)
    tipId = [4, 8, 12, 16, 20]
    if (len(lmList) != 0):
        fingers = []
        # thumb
        if (lmList[tipId[0]][1] > lmList[tipId[0] - 1][1]):
            fingers.append(1)
        else:
            fingers.append(0)
        # 4 fingers
        for id in range(1, len(tipId)):

            if (lmList[tipId[id]][2] < lmList[tipId[id] - 2][2]):
                fingers.append(1)

            else:
                fingers.append(0)

        cv2.rectangle(img, (20, 255), (170, 425), (0, 255, 0), cv2.FILLED)
        cv2.putText(img, str(getNumber(fingers)), (45, 375), cv2.FONT_HERSHEY_PLAIN,
                    10, (255, 0, 0), 20)

    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime
    cv2.putText(img, f'FPS: {int(fps)}', (400, 70), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 0), 3)
    cv2.imshow("image", img)
    if (cv2.waitKey(1) & 0xFF == ord('q')):
        break



