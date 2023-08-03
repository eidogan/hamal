import cv2
import mediapipe as mp
import time
import math
import numpy

class poseDetector():

    def __init__(self, static_image_mode=False, smooth_landmarks=True, model_complexity=1, min_detection_confidence=0.5, min_tracking_confidence=0.5):
        self.static_image_mode = static_image_mode
        self.smooth_landmarks = smooth_landmarks
        self.model_complexity = model_complexity
        self.min_detection_confidence = min_detection_confidence
        self.min_tracking_confidence = min_tracking_confidence

        self.mpPose = mp.solutions.pose
        self.pose = self.mpPose.Pose(self.static_image_mode, self.model_complexity, self.min_detection_confidence, self.min_tracking_confidence)
        self.mpDraw = mp.solutions.drawing_utils
        self.handIds = [15, 16, 17, 18, 19, 20, 21, 22]

    def findPose(self, img, draw=True):
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.pose.process(imgRGB)


        if self.results.pose_landmarks:
            for poseLms in self.results.pose_landmarks:
                if draw:
                    self.mpDraw.draw_landmarks(img, poseLms, self.mpPose.POSE_CONNECTIONS)

        return img

    def findPosition(self, img, poseNo=0, draw=True):
        xList = []
        yList = []
        bbox = []

        self.lmList = []

        if self.results.pose_landmarks:
            myHand = self.results.pose_landmarks[poseNo]

            for id, lm in enumerate(myPose.landmark):
            # print(id, lm)
                h, w, c = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                xList.append(cx)
                yList.append(cy)
            # print(id, cx, cy)
                self.lmList.append([id, cx, cy])

            if draw:

                xmin, xmax = min(xList), max(xList)
                ymin, ymax = min(yList), max(yList)
                bbox = xmin, ymin, xmax, ymax

            if draw:
                cv2.rectangle(img, (xmin - 20, ymin - 20), (xmax + 20, ymax + 20),
                (0, 255, 0), 2)

        return self.lmList, bbox
'''''
    def fingersUp(self):
        fingers = []
    # Thumb
        if self.lmList[self.tipIds[0]][1] > self.lmList[self.tipIds[0] - 1][1]:
            fingers.append(1)
        else:
            fingers.append(0)

    # Fingers
    
        for id in range(1, 5):

            if self.lmList[self.tipIds[id]][2] < self.lmList[self.tipIds[id] - 2][2]:
                fingers.append(1)
        
            else:
                fingers.append(0)

        totalFingers = fingers.count(1)

        return fingers
'''
    def findDistance(self, p1, p2, img, draw=True,r=15, t=3):
        x1, y1 = self.lmList[p1][1:]
        x2, y2 = self.lmList[p2][1:]
        cx, cy = (x1 + x2) // 2, (y1 + y2) // 2

        if draw:
            cv2.line(img, (x1, y1), (x2, y2), (255, 0, 255), t)
            cv2.circle(img, (x1, y1), r, (255, 0, 255), cv2.FILLED)
            cv2.circle(img, (x2, y2), r, (255, 0, 255), cv2.FILLED)
            cv2.circle(img, (cx, cy), r, (0, 0, 255), cv2.FILLED)
            length = math.hypot(x2 - x1, y2 - y1)

        else:
            length = math.hypot(x2 - x1, y2 - y1)

        return length, img, [x1, y1, x2, y2, cx, cy]

    def main():
        pTime = 0
        cTime = 0
        cap = cv2.VideoCapture(0)  # "rtsp://192.168.1.54/mjpg?source=1&cbr=0&quant=100&overlay=off")
        detector = poseDetector()

        while True:
            success, img = cap.read()
            img = cv2.flip(img, 1)
            img = detector.findPose(img)
            lmList, bbox = detector.findPosition(img)

            if len(lmList) != 0:
                print(lmList[4])

            cTime = time.time()
            fps = 1 / (cTime - pTime)
            pTime = cTime

            cv2.putText(img, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 255), 3)

            if cv2.waitKey(1) & 0xFF == 27:
                break

        cap.release()

    if __name__ == "__main__":
        main()
