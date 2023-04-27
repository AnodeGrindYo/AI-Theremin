def note_to_frequency(note: int) -> float:
    """
    Convert a MIDI note number to its corresponding frequency.

    :param note: The MIDI note number.
    :return: The frequency in Hz.
    """
    A4 = 440
    return A4 * (2**((note - 69) / 12))

def y_to_frequency(y: float, min_note: int = 24, max_note: int = 84) -> float:
    """
    Convert a y-coordinate to a frequency within a specified range.

    :param y: The y-coordinate as a percentage (0 to 100).
    :param min_note: The minimum MIDI note number. (default: 24, C1)
    :param max_note: The maximum MIDI note number. (default: 84, C6)
    :return: The corresponding frequency in Hz.
    """
    min_frequency = note_to_frequency(min_note)  # C1
    max_frequency = note_to_frequency(max_note)  # C6
    frequency = min_frequency + ((y/100) * (max_frequency - min_frequency))
    return frequency

def y_to_volume(y: float, min: int = 0, max: int = 100) -> float:
    """
    Convert a y-coordinate to a volume level within a specified range.

    :param y: The y-coordinate as a percentage (0 to 100).
    :param min: The minimum volume level. (default: 0)
    :param max: The maximum volume level. (default: 100)
    :return: The corresponding volume level.
    """
    volume = min +((y/100) * max - min)
    return volume