import threading
from concurrent.futures import process
from queue import Queue

import cv2


class StreamThread():
    __cam = None

    def __init__(self, camSrc=0, QSize=128) -> None:
        self.__stopped = False
        self.__Q = Queue(QSize)
        with process.ProcessPoolExecutor() as executor:
            executor.map(self.__init_webcam())

    def start(self):
        self.__thread = threading.Thread(target=self.update)
        self.__thread.daemon = True
        self.__thread.start()

    def update(self):
        while True:
            try:
                if self.__stopped:
                    self.stopStream()
                    break
                if not self.__Q.full():
                    isGrabbed, frame = self.__cam.read()
                if not isGrabbed:
                    print("frame not grbbed")
                    self.stopStream()
                    break
                self.__Q.put(frame)
            except Exception as e:
                print(e)

    def stopStream(self):
        self.__stopped = True
        self.__cam.release()
        cv2.destroyAllWindows()

    def readFrame(self):
        return self.__Q.get()

    def moreFrames(self):
        return self.__Q.qsize() > 0

    def getNoFrames(self):
        return self.__Q.qsize()

    def __init_webcam(self):
        self.__cam = cv2.VideoCapture(0)
        print("webcam started")
