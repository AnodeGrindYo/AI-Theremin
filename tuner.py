from typing import Tuple
import numpy as np

class Tuner:
    def __init__(self):
        self.note_names = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]

    def frequency_to_note(self, frequency: float) -> Tuple[str, float]:
        """
        Convert a frequency to a note name and the difference in cents from the target frequency.
        :param frequency: The input frequency.
        :return: A tuple containing the note name and the difference in cents.
        """
        if frequency == 0:
            return "-", 0

        note_number = 12 * (np.log2(frequency) - np.log2(440)) + 49
        note_index = round(note_number) % 12
        note_name = self.note_names[note_index]
        cents_difference = round((note_number - round(note_number)) * 100)

        return note_name, cents_difference