import pygame
import numpy as np
from typing import Tuple

SAMPLE_RATE = 44100
FADE_DURATION = 0.1
AMPLITUDE = 4096

def create_sine_wave(frequency: float, duration: float, volume: float, sample_rate: int = SAMPLE_RATE) -> np.ndarray:
    """
    Create a sine wave with the given frequency, duration, and volume.

    :param frequency: The frequency of the sine wave in Hz.
    :param duration: The duration of the sine wave in seconds.
    :param volume: The volume of the sine wave.
    :param sample_rate: The sample rate of the sine wave. (default: 44100)
    :return: The sine wave as a NumPy array.
    """
    samples = np.arange(duration * sample_rate)
    waveform = np.sin(2 * np.pi * frequency * samples / sample_rate)
    waveform_quiet = volume * waveform
    return waveform_quiet

def apply_fade(sine_wave: np.ndarray, fade_duration: float, sample_rate: int) -> np.ndarray:
    """
    Apply a fade in and fade out effect to the sine wave.

    :param sine_wave: The sine wave as a NumPy array.
    :param fade_duration: The duration of the fade effect in seconds.
    :param sample_rate: The sample rate of the sine wave.
    :return: The sine wave with the fade effect applied as a NumPy array.
    """
    fade_length = int(fade_duration * sample_rate)
    fade_in = np.linspace(0, 1, fade_length)
    fade_out = np.linspace(1, 0, fade_length)
    sine_wave[:fade_length] *= fade_in
    sine_wave[-fade_length:] *= fade_out
    return sine_wave

def play_sine_wave(frequency: float, duration: float, volume: float) -> pygame.mixer.Sound:
    """
    Play a sine wave with the given frequency, duration, and volume.

    :param frequency: The frequency of the sine wave in Hz.
    :param duration: The duration of the sine wave in seconds.
    :param volume: The volume of the sine wave.
    :return: The pygame Sound object playing the sine wave.
    """
    pygame.mixer.init()
    t = np.linspace(0, duration, int(SAMPLE_RATE * duration), False)

    normalized_volume = volume / 100  # Normalizes the voume
    adjusted_amplitude = AMPLITUDE * normalized_volume

    sine_wave = adjusted_amplitude * np.sin(frequency * t * 2 * np.pi)
    sine_wave = apply_fade(sine_wave, FADE_DURATION, SAMPLE_RATE)
    sine_wave = np.vstack((sine_wave, sine_wave)).T  # Creates a two-dimensional array for the stereo mixer
    sine_wave = np.ascontiguousarray(sine_wave.astype(np.int16))  # Makes the array contiguous
    sound = pygame.sndarray.make_sound(sine_wave)
    sound.play()
    return sound

def stop_sound(sound: pygame.mixer.Sound) -> None:
    """
    Stop the playback of the given pygame Sound object.

    :param sound: The pygame Sound object to stop.
    """
    sound.stop()
