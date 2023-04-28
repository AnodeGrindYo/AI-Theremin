import tkinter as tk
import math

class TunerCanvas(tk.Canvas):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)

    def draw_tuner(self, note: str, cents_diff: int):
        self.delete("all")  # Clear the canvas

        width = self.winfo_width()
        height = self.winfo_height()
        center_x, center_y = width // 2, height // 2

        circle_radius = min(width, height) // 4
        circle_color = self.calculate_color(cents_diff)

        # Draw the circle
        self.create_oval(center_x - circle_radius, center_y - circle_radius,
                         center_x + circle_radius, center_y + circle_radius,
                         fill=circle_color, outline="")

        # Draw the note text
        self.create_text(center_x, center_y, text=note, font=("Helvetica", circle_radius // 2, "bold"))

        # Draw the graduations and the cursor
        for i in range(-50, 51, 10):
            angle = math.radians(180 - (i * 180 / 50))
            line_length = circle_radius // 4 if i % 25 == 0 else circle_radius // 8
            start_x = center_x + (circle_radius + 5) * math.cos(angle)
            start_y = center_y - (circle_radius + 5) * math.sin(angle)
            end_x = center_x + (circle_radius + line_length + 5) * math.cos(angle)
            end_y = center_y - (circle_radius + line_length + 5) * math.sin(angle)
            self.create_line(start_x, start_y, end_x, end_y, width=2)

            # Draw the cursor
            if i == cents_diff:
                cursor_end_x = center_x + (circle_radius - 5) * math.cos(angle)
                cursor_end_y = center_y - (circle_radius - 5) * math.sin(angle)
                self.create_line(start_x, start_y, cursor_end_x, cursor_end_y, width=4, fill="black")

    def calculate_color(self, cents_diff: int) -> str:
        if abs(cents_diff) <= 5:
            return "green"
        elif abs(cents_diff) <= 15:
            return "yellow"
        elif abs(cents_diff) <= 30:
            return "orange"
        else:
            return "red"
