#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 28 07:52:36 2022

@author: sonounoteam

This script is dedicated to sonification based on a LHC data set
"""

from functools import cache
from pathlib import Path

import numpy as np

from sonounolib import Track

MAX_AMPLITUDE = np.iinfo('int16').max
DEFAULT_AMPLITUDE = MAX_AMPLITUDE / 16  # ~2048


@cache
def get_bip() -> Track:
    """Returns the bip sound.
    
    It represents the beginning of the particle track, at the center of the inner
    detector.
    """
    return Track.load(Path(__file__).parent / 'bip.wav', max_amplitude='int16')


def add_innersingletrack(sound: Track, duration: float = 2) -> None:
    """
    This method generates the sound of a track and return the associated audio `Track`.
    """
    sound.add_sine_wave('D6', duration, DEFAULT_AMPLITUDE)


def add_innerdoubletrack(sound: Track, duration: float = 2) -> None:
    """
    This method generates the sound of a double track and return the array.
    """
    cue = sound.duration
    sound.add_sine_wave('C6', duration, DEFAULT_AMPLITUDE)
    sound.set_cue_write(cue).add_sine_wave('D6', duration, DEFAULT_AMPLITUDE)


def add_tickmark_inner_calorimeter(sound: Track, duration: float = 0.1) -> None:
    """
    This method generate the sound of the tickmark that indicate the step from
    the inner detector to the green calorimeter and return the array.
    """
    sound.add_sine_wave('F7', duration, DEFAULT_AMPLITUDE)


def add_cluster(sound: Track, amplitude: float) -> None:
    """
    This method generate the sound of a cluster, setting the sound amplitude
    depending on the cluster energy, and return the array.
    """
    frequencies = [300, 350, 600, 800, 1000, 800, 800, 1000, 700, 600]
    if amplitude != 0:
        amplitude = amplitude * 2000 + 100
    for frequency in frequencies:
        sound.add_sine_wave(frequency, 0.1, amplitude)


def muontrack_with_cluster(amplitude: float) -> Track:
    """
    This method generates the sound of a muon track with cluster and returns
    the array. Includes tickmarks indicating the beginning and transition
    between inner detector and green calorimeter.
    """
    sound = get_bip()
    add_innersingletrack(sound)
    add_tickmark_inner_calorimeter(sound)
    cue = sound.duration
    add_cluster(sound, amplitude)
    add_innersingletrack(sound.set_cue_write(cue), duration=1)
    add_innersingletrack(sound)
    sound.add_blank(0.5)
    return sound


def singletrack_withcluster(amplitude: float) -> Track:
    """
    This method generates the sound of a single track with cluster and returns
    the array. It includes tickmarks indicating the beginning and transition
    between inner detector and green calorimeter.
    """
    sound = get_bip()
    add_innersingletrack(sound)
    add_tickmark_inner_calorimeter(sound)
    add_cluster(sound, amplitude)
    return sound


def doubletrack_withcluster(amplitude: float) -> Track:
    """
    This method generates the sound of a double track with cluster and returns
    the array. It includes tickmarks indicating the beginning and transition
    between inner detector and green calorimeter.
    """
    sound = get_bip()
    add_innerdoubletrack(sound)
    add_tickmark_inner_calorimeter(sound)
    add_cluster(sound, amplitude)
    return sound


def singletrack_only() -> Track:
    """
    This method generates the sound of a simple track without cluster and returns
    the array. It includes tickmarks indicating the beginning and transition
    between inner detector and green calorimeter.
    """
    sound = get_bip()
    add_innersingletrack(sound)
    add_tickmark_inner_calorimeter(sound)
    return sound


def doubletrack_only() -> Track:
    """
    This method generates the sound of a double track without cluster and returns
    the array. It includes tickmarks indicating the beginning and transition
    between inner detector and green calorimeter.
    """
    sound = get_bip()
    add_innerdoubletrack(sound)
    add_tickmark_inner_calorimeter(sound)
    return sound


def cluster_only(amplitude: float) -> Track:
    """
    This method generates the sound of a cluster (taking in consideration the
    cluster energy) and returns the array. It includes tickmarks indicating the
    beginning and transition between inner detector and green calorimeter.
    """
    sound = get_bip()
    sound.add_blank(2)
    add_tickmark_inner_calorimeter(sound)
    add_cluster(sound, amplitude)
    return sound
