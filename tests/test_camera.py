import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import cv2
import pytest
from camera import Camera
import numpy as np

# def test_camera_initialization():
#     """
#     Test the initialization of the Camera class.
#     """
#     camera = Camera()
#     assert isinstance(camera.video_capture, cv2.VideoCapture)

# def test_camera_read():
#     """
#     Test if the Camera class's read() method returns a valid image.
#     Note: This test may fail if no camera is available on the machine.
#     """
#     camera = Camera()
#     ret, image = camera.read()
#     assert isinstance(ret, bool)
#     assert ret  # Check if the capture was successful
#     assert isinstance(image, np.ndarray)
#     camera.release()

# def test_camera_flip_horizontal():
#     """
#     Test if the Camera class's flip_horizontal() method returns a flipped image with the correct dimensions.
#     Note: This test may fail if no camera is available on the machine.
#     """
#     camera = Camera()
#     ret, image = camera.read()
#     if ret:
#         flipped_image = camera.flip_horizontal(image)
#         assert isinstance(flipped_image, np.ndarray)
#         assert flipped_image.shape == image.shape
#     camera.release()

# def test_camera_release():
#     """
#     Test if the Camera class's release() method properly releases the camera resources.
#     """
#     camera = Camera()
#     camera.release()
#     assert not camera.video_capture.isOpened()