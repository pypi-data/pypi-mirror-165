"""
This script was used to test the values of amplitude related to the volume
feature of the sound.
"""
from sonounolib import Track

track = Track(max_amplitude='int16')
track.add_sine_wave(440, 1, 100)
track.add_sine_wave(440, 1, 500)
track.add_sine_wave(440, 1, 1000)
track.add_sine_wave(440, 1, 2000)
track.play()
