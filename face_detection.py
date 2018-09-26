import concurrent.futures.process as processor

import cv2

from face_recognizer import *
from stream_thread import StreamThread

facial_features = [
    'chin',
    'left_eyebrow',
    'right_eyebrow',
    'nose_bridge',
    'nose_tip',
    'left_eye',
    'right_eye',
    'top_lip',
    'bottom_lip'
]

WIDTH = 640
HEIGHT = 480

SCALE_FACTOR = 10
WINDOW = "Real Time Video"


class FaceDetector:
    def __init__(self) -> None:
        super().__init__()
        self.process_this_frame = True
        self.streamThread = StreamThread()
        self.streamThread.start()
        self.faceRecognizer = FaceRecognizer()
        self.faceRecognizer.trainModel()
        cv2.namedWindow(WINDOW, cv2.WINDOW_NORMAL)

    def getFrame(self):
        return self.frame

    def startStream(self):
        while self.streamThread.moreFrames():
            self.frame = self.streamThread.readFrame()
            if self.process_this_frame:
                with processor.ProcessPoolExecutor() as executor:
                    executor.map(self.__processFrame())
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
            cv2.imshow(WINDOW, self.frame)
            self.process_this_frame = not self.process_this_frame
            cv2.waitKey(1)

    def __processFrame(self):
        small = 1 / SCALE_FACTOR
        small_frame = cv2.resize(self.frame, (0, 0), fx=small, fy=small)
        rgb_frame = small_frame[:, :, ::-1]
        self.__detect_face(rgb_frame)

    def __detect_face(self, rgb_frame):
        face_locations = face_recognition.face_locations(rgb_frame)
        if len(face_locations) > 0:
            # self.__showLandmark(rgb_frame, face_locations)
            t = time.time()
            matches = self.faceRecognizer.findMatch(rgb_frame, face_locations)
            print(time.time() - t)
        for (top, right, bottom, left) in face_locations:
            top *= SCALE_FACTOR
            right *= SCALE_FACTOR
            bottom *= SCALE_FACTOR
            left *= SCALE_FACTOR
            cv2.putText(self.frame, matches[0], (left + 6, bottom - 6), cv2.FONT_HERSHEY_DUPLEX, 1.0, (255, 255, 255),
                        1)
            cv2.rectangle(self.frame, (left, top), (right, bottom), (0, 255, 0), 2, )

    def __showLandmark(self, rgb_frame, face_locations):
        facial_landmarks = face_recognition.face_landmarks(rgb_frame, face_locations)
        for landmark in facial_landmarks:
            for facial_feature in facial_features:
                for point in landmark[facial_feature]:
                    x = point[0] * SCALE_FACTOR
                    y = point[1] * SCALE_FACTOR
                    cv2.line(self.frame, (x, y), (x, y), (0, 0, 255), 2)
