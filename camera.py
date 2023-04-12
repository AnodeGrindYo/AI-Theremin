import cv2

class Camera:
    def __init__(self, device_id=0):
        self.video_capture = cv2.VideoCapture(device_id)

    def read(self):
        return self.video_capture.read()

    def flip_horizontal(self, image):
        return cv2.flip(image, 1)

    def release(self):
        self.video_capture.release()
        cv2.destroyAllWindows()
