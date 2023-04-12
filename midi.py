def note_to_frequency(note):
    A4 = 440
    return A4 * (2**((note - 69) / 12))

def y_to_frequency(y, min_note=24, max_note=84):
    min_frequency = note_to_frequency(min_note)  # C1
    max_frequency = note_to_frequency(max_note)  # C6
    frequency = min_frequency + ((y/100) * (max_frequency - min_frequency))
    return frequency

def y_to_volume(y, min=0, max=100):
    volume = min +((y/100) * max - min)
    return volume