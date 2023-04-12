import pygame
import numpy as np

SAMPLE_RATE = 44100
FADE_DURATION = 0.1
AMPLITUDE = 4096

def create_sine_wave(frequency, duration, volume, sample_rate=SAMPLE_RATE):
    samples = np.arange(duration * sample_rate)
    waveform = np.sin(2 * np.pi * frequency * samples / sample_rate)
    waveform_quiet = volume * waveform
    return waveform_quiet

def apply_fade(sine_wave, fade_duration, sample_rate):
    fade_length = int(fade_duration * sample_rate)
    fade_in = np.linspace(0, 1, fade_length)
    fade_out = np.linspace(1, 0, fade_length)
    sine_wave[:fade_length] *= fade_in
    sine_wave[-fade_length:] *= fade_out
    return sine_wave

def play_sine_wave(frequency, duration, volume):
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

def stop_sound(sound):
    sound.stop()
