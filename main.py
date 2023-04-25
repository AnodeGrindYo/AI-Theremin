import cv2
import tkinter as tk
from PIL import ImageTk
import time
import PIL
import tkinter
import hand_tracking
import midi
import mediapipe_utils
from camera import Camera
import oscillator
from smoothing import DataSmoother
from gui import ThereminGUI
from numpy import ndarray
from typing import Tuple, Optional, Dict

quit_flag = False
# Create DataSmoother instances for frequency and volume
frequency_smoother = DataSmoother()
volume_smoother = DataSmoother()


def on_closing() -> None:
    """
    Set the global quit_flag to True and destroy the theremin_gui root window.

    This function is typically used as a callback for handling the closing event
    of the theremin_gui application window. It sets the global quit_flag to True
    to signal the main update loop to exit, and then destroys the root window
    of the theremin_gui, effectively closing the application.
    """
    global quit_flag
    quit_flag = True
    theremin_gui.root.destroy()
    
def read_camera() -> ndarray:
    """
    Read a frame from the camera and flip it horizontally.

    This function reads a frame from the camera, flips it horizontally, and
    returns the modified frame. Flipping the frame horizontally is useful for
    creating a mirror effect, which is often more intuitive for users when
    interacting with applications that involve hand tracking and gesture recognition.

    Returns:
        frame (numpy.ndarray): The captured and horizontally flipped frame.
    """
    success, frame = camera.read()
    frame = camera.flip_horizontal(frame)
    return frame

def process_frame(frame: ndarray) -> Tuple[ndarray, dict]:
    """
    Process the input frame using hand_tracking.process_image.

    This function processes the input frame using the hand_tracking.process_image function.
    It uses the hand_detector, drawing_utils, and connections_draw_spec objects to detect
    and draw hand landmarks on the frame.

    Args:
        frame (numpy.ndarray): The input frame to be processed.

    Returns:
        Tuple[numpy.ndarray, dict]: A tuple containing the processed frame with drawn hand landmarks
                                    and a dictionary containing hand coordinates.
    """
    return hand_tracking.process_image(frame, hand_detector, drawing_utils, connections_draw_spec)

def update_smoothing_factors(smoothing_factor: Optional[float]) -> None:
    """
    Update the smoothing factors of the frequency_smoother and volume_smoother objects.

    This function updates the smoothing factors of the frequency_smoother and
    volume_smoother objects if a valid smoothing_factor value is provided.

    Args:
        smoothing_factor (Optional[float]): The new smoothing factor value to be set for both
                                            frequency_smoother and volume_smoother objects.
                                            If None, no update will be performed.
    """
    if smoothing_factor is not None:
        frequency_smoother.smoothing_factor = smoothing_factor
        volume_smoother.smoothing_factor = smoothing_factor

def update_change_limits(change_limit: Optional[float]) -> None:
    """
    Update the smoothing factors of the frequency_smoother and volume_smoother objects.

    This function updates the smoothing factors of the frequency_smoother and
    volume_smoother objects if a valid smoothing_factor value is provided.

    Args:
        smoothing_factor (Optional[float]): The new smoothing factor value to be set for both
                                            frequency_smoother and volume_smoother objects.
                                            If None, no update will be performed.
    """
    if change_limit is not None:
        frequency_smoother.change_limit = change_limit
        volume_smoother.change_limit = change_limit

def update_hands_display(frame: ndarray, hands_coord: Dict[str, Dict[str, float]]) -> None:
    """
    Update the hands display on the frame with the given hand coordinates.

    This function iterates through the hand coordinates and displays the X and Y
    coordinates of each hand (Right or Left) on the input frame.

    Args:
        frame (numpy.ndarray): The input frame on which to display the hand coordinates.
        hands_coord (Dict[str, Dict[str, float]]): A dictionary containing hand coordinates.
                                                  The keys are 'Right' and/or 'Left', and the
                                                  values are dictionaries with 'x' and 'y' keys
                                                  and float values.
    """
    for hand, coords in hands_coord.items():
        display_text(frame, f"{hand} X: {hands_coord[hand]['x']:.2f}", (7, 110 if hand == 'Right' else 170), font_scale=1.5)
        display_text(frame, f"{hand} Y: {hands_coord[hand]['y']:.2f}", (7, 140 if hand == 'Right' else 200), font_scale=1.5)

def update_frequency_and_volume_labels(
        hands_coord: Dict[str, Dict[str, float]],
        previous_volume: float
    ) -> Tuple[float, float]:
    """
    Update the frequency and volume labels based on the given hand coordinates.

    This function updates the frequency and volume labels based on the hand coordinates.
    It calculates the frequency and volume values, smooths them using the frequency_smoother
    and volume_smoother objects, and updates the corresponding labels.

    Args:
        hands_coord (Dict[str, Dict[str, float]]): A dictionary containing hand coordinates.
                                                  The keys are 'Right' and/or 'Left', and the
                                                  values are dictionaries with 'x' and 'y' keys
                                                  and float values.
        previous_volume (float): The previous volume value.

    Returns:
        Tuple[float, float]: A tuple containing the smoothed frequency and volume values.
    """
    smooth_frequency = None
    smooth_volume = None
    
    if "Right" in hands_coord:
        frequency = midi.y_to_frequency(hands_coord["Right"]["y"])
        smooth_frequency = frequency_smoother.smooth(frequency)
        frequency_label.config(text=f"Freq : {smooth_frequency:.2f}")

    if "Left" in hands_coord:
        volume = midi.y_to_volume(hands_coord["Left"]["y"])
        smooth_volume = volume_smoother.smooth(volume)
        volume_label.config(text=f"Vol : {smooth_volume:.0f}")
    else:
        smooth_volume = volume_smoother.smooth(previous_volume)

    return smooth_frequency, smooth_volume

def play_sound(
        smooth_frequency: float, 
        smooth_volume: float, 
        previous_frequency: float, 
        previous_volume: float
    ) -> Tuple[float, float, float]:
    """
    Play a sine wave sound based on the given smoothed frequency and volume values.

    This function plays a sine wave sound if the difference between the current smoothed
    frequency (smooth_frequency) and the previous frequency (previous_frequency) is greater
    than 1, or if the difference between the current smoothed volume (smooth_volume) and
    the previous volume (previous_volume) is greater than 1. If a sound was playing, it
    stops the previous sound and plays a new sound with the current smoothed frequency
    and volume. Finally, it updates the previous_frequency and previous_volume variables
    with the new smoothed values.

    Args:
        smooth_frequency (float): The current smoothed frequency value.
        smooth_volume (float): The current smoothed volume value.
        previous_frequency (float): The previous frequency value.
        previous_volume (float): The previous volume value.

    Returns:
        Tuple[float, float, float]: A tuple containing the sound object, the updated
                                     previous_frequency, and the updated previous_volume.
    """
    sound = None
    if (smooth_frequency is None) or (previous_frequency is None) or (smooth_volume is None) or (previous_volume is None):
        return None, None, None
    
    if abs(smooth_frequency - previous_frequency) > 1 or abs(smooth_volume - previous_volume) > 1:
        if sound:
            oscillator.stop_sound(sound)
        sound = oscillator.play_sine_wave(smooth_frequency, 1, smooth_volume)
        previous_frequency = smooth_frequency
        previous_volume = smooth_volume

    return sound, previous_frequency, previous_volume

def update_canvas(frame: ndarray) -> None:
    """
    Update the canvas with the given frame.

    This function converts the input frame from BGR to RGB, creates a PhotoImage
    object from the frame, and then updates the canvas with the new image.

    Args:
        frame (numpy.ndarray): The input frame to display on the canvas.
    """
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    photo = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(frame))
    canvas.create_image(0, 0, image=photo, anchor=tkinter.NW)

def update_framerate(previous_time: float) -> float:
    """
    Update the framerate label and calculate the new previous_time.

    This function calculates the current framerate, updates the framerate label
    with the calculated framerate, and updates the previous_time variable.

    Args:
        previous_time (float): The previous timestamp used to calculate the framerate.

    Returns:
        float: The updated previous_time value.
    """
    current_time = time.time()
    framerate = 1 / (current_time - previous_time)
    previous_time = current_time
    framerate_label.config(text=f"FPS: {framerate:.0f}")

    return previous_time

def update_loop(
        theremin_gui: "ThereminGUI", 
        smoothing_factor: Optional[float] = None, 
        change_limit: Optional[float] = None
    ) -> None:
    """
    Main loop for updating the theremin GUI, processing frames, and playing sounds.

    This function reads frames from the camera, processes them to detect hands,
    updates the theremin GUI, sets smoothing factors and change limits, updates
    the hands display, calculates smoothed frequency and volume, plays sounds
    based on the calculated values, updates the canvas, and updates the framerate.

    Args:
        theremin_gui (ThereminGUI): The theremin GUI instance.
        smoothing_factor (Optional[float]): The smoothing factor for frequency and volume, if any.
        change_limit (Optional[float]): The change limit for frequency and volume, if any.
    """
    global hand_detector, drawing_utils, connections_draw_spec, canvas, hands_coord
    previous_time = 0
    previous_frequency = 0
    previous_volume = 0

    while True:
        frame = read_camera()
        frame, hands_coord = process_frame(frame)

        if quit_flag:
            break
        
        theremin_gui.root.update()
        
        update_smoothing_factors(smoothing_factor)
        update_change_limits(change_limit)
        update_hands_display(frame, hands_coord)
        
        smooth_frequency, smooth_volume = update_frequency_and_volume_labels(hands_coord, previous_volume)
        if smooth_frequency is not None and smooth_volume is not None:
            sound, previous_frequency, previous_volume = play_sound(smooth_frequency, smooth_volume, previous_frequency, previous_volume)
            
            if sound is not None and previous_frequency is not None and previous_volume is not None:
                # update_canvas(frame)
                theremin_gui.update_canvas(frame)
                previous_time = update_framerate(previous_time)

        if quit_flag:
            break

def display_text(
        image: ndarray, 
        text: str, 
        position: tuple[int, int], 
        font_scale: float = 1.5, 
        font: int = cv2.FONT_HERSHEY_PLAIN, 
        color: tuple[int, int, int] = (217, 0, 234), 
        thickness: int = 3
    ) -> None:
    """
    Display text on an image at the specified position.

    This function puts the given text on the input image at the given position
    with specified font, font scale, color, and thickness.

    Args:
        image (np.ndarray): The input image.
        text (str): The text to display on the image.
        position (tuple[int, int]): The x and y coordinates of the text position on the image.
        font_scale (float, optional): The scale factor of the font. Default is 1.5.
        font (int, optional): The font type from OpenCV's font options. Default is cv2.FONT_HERSHEY_PLAIN.
        color (tuple[int, int, int], optional): The color of the text in BGR format. Default is (217, 0, 234).
        thickness (int, optional): The thickness of the text. Default is 3.
    """
    cv2.putText(image, text, position, font, font_scale, color, thickness)


camera = Camera()
hand_detector, drawing_utils, connections_draw_spec = mediapipe_utils.init_mediapipe()

previous_time = 0
current_time = 0
hands_coord = {}

# Create an instance of ThereminGUI
theremin_gui = ThereminGUI(update_loop, on_closing)
canvas = theremin_gui.canvas
frequency_label = theremin_gui.frequency_label
volume_label = theremin_gui.volume_label
framerate_label = theremin_gui.framerate_label

# # Start the update loop
# update_loop(theremin_gui.root)
update_loop(theremin_gui)
theremin_gui.start()

# Start the ThereminGUI
theremin_gui.start()

camera.release()
