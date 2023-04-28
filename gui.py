import tkinter as tk
from tkinter import Scale, HORIZONTAL
from functools import partial
from PIL import Image, ImageTk
import cv2
from tuner import Tuner
from typing import Callable
from tuner_canvas import TunerCanvas


class ThereminGUI:
    """A GUI class for Theremin."""
    
    def __init__(self, update_loop: Callable, on_closing: Callable) -> None:
        """
        Initialize the Theremin GUI.

        :param update_loop: The function to call for updating the GUI.
        :param on_closing: The function to call when the GUI window is closed.
        """
        self.root = tk.Tk()
        self.root.protocol("WM_DELETE_WINDOW", on_closing)
        self.root.title("Theremin")
        self.smoothing_factor = 0.5
        self.change_limit = 50
        self.tuner = Tuner()
        

        # Create the canvas
        self.canvas = self.create_canvas()

        # Create the right frame
        right_frame = self.create_right_frame()

        # Create frequency_label
        self.frequency_label = self.create_frequency_label(right_frame)

        # Create volume_label
        self.volume_label = self.create_volume_label(right_frame)

        # Create framerate_label
        self.framerate_label = self.create_framerate_label(right_frame)

        # Create smoothing_factor slider
        self.smoothing_factor_slider = self.create_smoothing_factor_slider(right_frame)

        # Create change_limit slider
        self.change_limit_slider = self.create_change_limit_slider(right_frame)
        
        # # Create tuner_label
        # self.tuner_label = self.create_tuner_label(right_frame)
        
        # Create tuner_canvas
        self.tuner_canvas = self.create_tuner_canvas(right_frame)
    
    def update_canvas(self, frame: cv2.Mat) -> None: 
        """
        Update the canvas with the given frame.

        :param frame: The frame to display on the canvas.
        """
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        pil_image = Image.fromarray(frame_rgb)
        self.canvas_image = ImageTk.PhotoImage(pil_image)
        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.canvas_image)
    
    def create_canvas(self) -> tk.Canvas:
        canvas = tk.Canvas(self.root, width=640, height=480)
        canvas.grid(column=0, row=0)
        return canvas
    
    def create_right_frame(self) -> tk.Frame:
        right_frame = tk.Frame(self.root)
        right_frame.grid(column=1, row=0, padx=10)
        return right_frame

    def create_frequency_label(self, parent: tk.Widget) -> tk.Label:
        frequency_label = tk.Label(parent)
        frequency_label.pack()
        return frequency_label

    def create_volume_label(self, parent: tk.Widget) -> tk.Label:
        volume_label = tk.Label(parent)
        volume_label.pack()
        return volume_label

    def create_framerate_label(self, parent: tk.Widget) -> tk.Label:
        framerate_label = tk.Label(parent, width=50)
        framerate_label.pack()
        return framerate_label

    def create_smoothing_factor_slider(self, parent: tk.Widget) -> Scale:
        smoothing_factor_label = tk.Label(parent, text="Smoothing Factor (0 - 1):")
        smoothing_factor_label.pack()
        smoothing_factor_slider = Scale(
            parent,
            from_=0, to=1,
            resolution=0.01,
            orient=HORIZONTAL,
            command=lambda x: setattr(self, 'smoothing_factor', float(x))
        )
        smoothing_factor_slider.set(0.5)
        smoothing_factor_slider.pack()
        return smoothing_factor_slider

    def create_change_limit_slider(self, parent: tk.Widget) -> Scale:
        change_limit_label = tk.Label(parent, text="Change Limit (0 - 100):")
        change_limit_label.pack()
        change_limit_slider = Scale(
            parent,
            from_=0,
            to=100,
            resolution=1,
            orient=HORIZONTAL,
            command=lambda x: setattr(self, 'change_limit', int(x))
        )
        change_limit_slider.set(50)
        change_limit_slider.pack()
        return change_limit_slider
    
    def create_tuner_label(self, parent: tk.Widget) -> tk.Label:
        tuner_label = tk.Label(parent)
        tuner_label.pack()
        return tuner_label

    def update_tuner_label(self, frequency: float) -> None:
        note_name, cents_difference = self.tuner.frequency_to_note(frequency)
        self.tuner_label.config(text=f"Note: {note_name} ({cents_difference:+} cents)")
    
    def create_tuner_canvas(self, parent: tk.Widget) -> TunerCanvas:
        tuner_canvas = TunerCanvas(parent, width=300, height=300, bg="white")
        tuner_canvas.pack()
        return tuner_canvas

    def update_tuner_canvas(self, frequency: float) -> None:
        note_name, cents_difference = self.tuner.frequency_to_note(frequency)
        self.tuner_canvas.draw_tuner(note_name, cents_difference)
    
    def update(self) -> None:
        """
        Update the GUI.
        """
        smoothing_factor = self.smoothing_factor_slider.get()
        change_limit = self.change_limit_slider.get()
        self.update_loop(self, smoothing_factor=smoothing_factor, change_limit=change_limit)
        

    def start(self) -> None:
        """
        Start the main loop of the GUI.
        """
        self.root.after(0, self.update)
        self.root.mainloop()

