import cv2
import settings
import time
log = settings.logging

class VideoCamera(object):
    def __init__(self):
        self.video = cv2.VideoCapture(0)
        log.debug("Init Camera")

    def __del__(self):
        self.video.release()

    def get_frame(self, color=True):

        success, image = self.video.read()
        time.sleep(0.5)

        if not color:
            image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        ret, jpeg = cv2.imencode('.jpg', image)

        return image.tobytes()



