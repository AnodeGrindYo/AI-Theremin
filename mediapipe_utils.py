import cv2
import mediapipe as mp
from mediapipe.python.solutions.hands import Hands
from mediapipe.python.solutions.drawing_utils import DrawingSpec

# TODO check missing types

def init_mediapipe():
    """
    Initialize Mediapipe Hand detector and drawing utilities.

    :return: A tuple containing the hand detector, drawing utilities, and connections drawing specifications.
    """
    media_pipe_hands = mp.solutions.hands
    hand_detector = media_pipe_hands.Hands()
    drawing_utils = mp.solutions.drawing_utils
    connections_draw_spec = drawing_utils.DrawingSpec(color=(198, 189, 10), thickness=2, circle_radius=1)

    return hand_detector, drawing_utils, connections_draw_spec

def process_image(hand_detector: Hands, image: cv2.Mat):
    """
    Process the image using the Mediapipe Hand detector.

    :param hand_detector: The hand detector instance.
    :param image: The input image.
    :return: The detected hand landmarks.
    """
    return hand_detector.process(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))

def draw_landmarks(
        image: cv2.Mat, 
        hand_landmarks, 
        drawing_utils,
        connections_draw_spec: DrawingSpec, 
        display_camera_image: bool = False
    ) -> None:
    """
    Draw hand landmarks on the input image.

    :param image: The input image.
    :param hand_landmarks: The detected hand landmarks.
    :param drawing_utils: The drawing utilities.
    :param connections_draw_spec: The drawing specifications for hand connections.
    :param display_camera_image: Whether to display the camera image or not. (default: False)
    """
    drawing_utils.draw_landmarks(
        image,
        hand_landmarks,
        mp.solutions.hands.HAND_CONNECTIONS,
        connections_draw_spec,
        connections_draw_spec
    )
