import cv2
from typing import Tuple, Union

class Camera:
    """Class representing a camera to capture images."""
    
    def __init__(self, device_id: int = 0) -> None:
        """
        Initialize the camera with the specified device ID.

        :param device_id: Camera device ID (default: 0)
        """
        self.video_capture = cv2.VideoCapture(device_id)

    def read(self) -> Tuple[bool, Union[None, cv2.Mat]]:
        """
        Capture an image from the camera.

        :return: Tuple (ret, image), where ret is a boolean indicating if the capture was successful and image is the captured image.
        """
        return self.video_capture.read()

    def flip_horizontal(self, image: cv2.Mat) -> cv2.Mat:
        """
        Flip an image horizontally.

        :param image: Image to flip.
        :return: Horizontally flipped image.
        """
        return cv2.flip(image, 1)

    def release(self) -> None:
        """
        Release the camera resources and destroy all opened windows.
        """
        self.video_capture.release()
        cv2.destroyAllWindows()
        try:
            cv2.destroyAllWindows()
        except cv2.error as e:
            print(f"Warning: Could not destroy windows: {e}")
