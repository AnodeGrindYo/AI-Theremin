import tkinter as tk
from tkinter import Scale, HORIZONTAL
from functools import partial
from PIL import Image, ImageTk
import cv2



class ThereminGUI:
    def __init__(self, update_loop, on_closing):
        self.root = tk.Tk()
        self.root.protocol("WM_DELETE_WINDOW", on_closing)
        self.root.title("Theremin")
        self.smoothing_factor = 0.5
        self.change_limit = 50

        # Create the canvas
        self.canvas = tk.Canvas(self.root, width=640, height=480)
        self.canvas.grid(column=0, row=0)

        # Create the right frame
        right_frame = tk.Frame(self.root)
        right_frame.grid(column=1, row=0, padx=10)

        # Create frequency_label
        self.frequency_label = tk.Label(right_frame)
        self.frequency_label.pack()

        # Create volume_label
        self.volume_label = tk.Label(right_frame)
        self.volume_label.pack()

        # Create framerate_label
        self.framerate_label = tk.Label(right_frame, width=50)
        self.framerate_label.pack()

        # Create smoothing_factor slider
        smoothing_factor_label = tk.Label(right_frame, text="Smoothing Factor (0 - 1):")
        smoothing_factor_label.pack()
        self.smoothing_factor_slider = Scale(
            right_frame, 
            from_=0, to=1, 
            resolution=0.01, 
            orient=HORIZONTAL, 
            command=lambda x: setattr(self, 'smoothing_factor', float(x))
        )
        self.smoothing_factor_slider.set(0.5)
        
        self.smoothing_factor_slider.pack()

        # Create change_limit slider
        change_limit_label = tk.Label(right_frame, text="Change Limit (0 - 100):")
        change_limit_label.pack()
        self.change_limit_slider = Scale(
            right_frame, 
            from_=0, 
            to=100, 
            resolution=1, 
            orient=HORIZONTAL, 
            command=lambda x: setattr(self, 'change_limit', int(x))
        )
        self.change_limit_slider.set(50)
        self.change_limit_slider.pack()
    
    def update_canvas(self, frame): 
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        pil_image = Image.fromarray(frame_rgb)
        self.canvas_image = ImageTk.PhotoImage(pil_image)
        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.canvas_image)
    
    def update(self):
        smoothing_factor = self.smoothing_factor_slider.get()
        change_limit = self.change_limit_slider.get()
        self.update_loop(self, smoothing_factor=smoothing_factor, change_limit=change_limit)

    def start(self):
        self.root.after(0, self.update)
        self.root.mainloop()

