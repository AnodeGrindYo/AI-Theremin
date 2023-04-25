import cv2
from mediapipe_utils import draw_landmarks
import numpy as np

def normalize_coordinates(coord, max_value, min_value=0):
    return (coord - min_value) / (max_value - min_value) * 100

def clip_coordinates(value):
    return max(0, min(value, 100))

def process_hand(hand_landmarks, hand_classification, coord_x, coord_y, image_shape):
    normalized_x = clip_coordinates(normalize_coordinates(coord_x, image_shape[1]))
    normalized_y = clip_coordinates(100-normalize_coordinates(coord_y, image_shape[0]))  # Inversion de l'axe Y

    hands_coord = {hand_classification: {"x": normalized_x, "y": normalized_y}}
    return hands_coord

def process_image(image, hand_detector, drawing_utils, connections_draw_spec, display_camera_image=False):
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    detection_results = hand_detector.process(image_rgb)
    hands_coord = {}
    
    black_image = np.zeros_like(image) if not display_camera_image else None

    if detection_results.multi_hand_landmarks:
        for index, hand_landmarks in enumerate(detection_results.multi_hand_landmarks):
            hand_classification = detection_results.multi_handedness[index].classification[0].label
            index_tip = hand_landmarks.landmark[8]

            coord_x, coord_y = float(index_tip.x * image.shape[1]), float(index_tip.y * image.shape[0])

            hands_coord.update(process_hand(hand_landmarks, hand_classification, coord_x, coord_y, image.shape))
            draw_landmarks(
                black_image if not display_camera_image else image, 
                hand_landmarks, 
                drawing_utils, 
                connections_draw_spec,  
                display_camera_image
            )
            
    if not display_camera_image:
        image[:] = black_image[:]

    return image, hands_coord