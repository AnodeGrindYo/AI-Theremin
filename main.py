import tkinter as tk
from PIL import Image, ImageTk
import cv2
import time
import PIL
import tkinter
import hand_tracking
import midi
import mediapipe_utils
from camera import Camera
import oscillator

quit_flag = False

def on_closing():
    global quit_flag
    quit_flag = True
    root.destroy()

def update_loop():
    global root, hand_detector, drawing_utils, connections_draw_spec, canvas, hands_coord
    previous_time = 0
    sound = None
    volume = 0
    frequency = 0
    previous_frequency = 0
    previous_volume = 0

    while True:
        success, frame = camera.read()
        frame = camera.flip_horizontal(frame)
        frame, hands_coord = hand_tracking.process_image(frame, hand_detector, drawing_utils, connections_draw_spec)
        
        # Updates hands display and FPS
        for hand, coords in hands_coord.items():
            display_text(frame, f"{hand} X: {hands_coord[hand]['x']:.2f}", (7, 110 if hand == 'Right' else 170), font_scale=1.5)
            display_text(frame, f"{hand} Y: {hands_coord[hand]['y']:.2f}", (7, 140 if hand == 'Right' else 200), font_scale=1.5)
            
            # Updates frequency display
            if "Right" in hands_coord:
                frequency = midi.y_to_frequency(hands_coord["Right"]["y"])
                frequency_label.config(text=f"Freq : {frequency:.2f}")
                
            # Updates Volume display
            if "Left" in hands_coord:
                volume = midi.y_to_volume(hands_coord["Left"]["y"])
                volume_label.config(text=f"Vol : {volume:.0f}")
            else:
                volume = previous_volume
                
            # Produces sound
            if abs(frequency - previous_frequency) > 1 or abs(volume - previous_volume) > 1:
                if sound:
                    oscillator.stop_sound(sound)
                sound = oscillator.play_sine_wave(frequency, 1, volume)
                previous_frequency = frequency
                previous_volume = volume
        
        # Converts image to PhotoImage for display on canvas
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        photo = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(frame))
        canvas.create_image(0, 0, image=photo, anchor=tkinter.NW)
        
        # Updates framerate display
        current_time = time.time()
        framerate = 1 / (current_time - previous_time)
        previous_time = current_time
        framerate_label.config(text=f"FPS: {framerate:.0f}")
        
        root.update()

        if quit_flag:
            break


def display_text(image, text, position, font_scale=1.5, font=cv2.FONT_HERSHEY_PLAIN, color=(217, 0, 234), thickness=3):
    cv2.putText(image, text, position, font, font_scale, color, thickness)

camera = Camera()
hand_detector, drawing_utils, connections_draw_spec = mediapipe_utils.init_mediapipe()

previous_time = 0
current_time = 0
hands_coord = {}

root = tk.Tk()
root.protocol("WM_DELETE_WINDOW", on_closing)
root.title("Theremin")

# Create the canvas
canvas = tk.Canvas(root, width=640, height=480)
canvas.grid(column=0, row=0)

# Create the right frame
right_frame = tk.Frame(root)
right_frame.grid(column=1, row=0, padx=10)

# Create frequency_label
frequency_label = tk.Label(right_frame)
frequency_label.grid(column=0, row=0)
frequency_label.pack()

# Create volume_label
volume_label = tk.Label(right_frame)
volume_label.pack()

# Create framerate_label
framerate_label = tk.Label(right_frame, width=50)
framerate_label.pack()

update_loop()

root.mainloop()

camera.release()
