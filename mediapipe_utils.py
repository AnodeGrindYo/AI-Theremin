import cv2
import mediapipe as mp

def init_mediapipe():
    media_pipe_hands = mp.solutions.hands
    hand_detector = media_pipe_hands.Hands()
    drawing_utils = mp.solutions.drawing_utils
    connections_draw_spec = drawing_utils.DrawingSpec(color=(198, 189, 10), thickness=2, circle_radius=1)

    return hand_detector, drawing_utils, connections_draw_spec

def process_image(hand_detector, image):
    return hand_detector.process(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))

def draw_landmarks(image, hand_landmarks, drawing_utils, connections_draw_spec,  display_camera_image=False):
    drawing_utils.draw_landmarks(
        image,
        hand_landmarks,
        mp.solutions.hands.HAND_CONNECTIONS,
        connections_draw_spec,
        connections_draw_spec
    )
