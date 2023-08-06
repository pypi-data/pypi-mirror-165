#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 28 07:51:54 2022

@author: sonounoteam

This script is dedicated to 3D plot generation based on a LHC data set
"""

import numpy as np

from .models import ParticleTrack


class ColorGetter:
    """A class to loop though a list of defined colors."""
    COLORS = [
        'blue',
        'orange',
        'green',
        'red',
        'purple',
        'brown',
        'pink',
        'grey',
        'olive',
        'cyan',
    ]

    def __init__(self) -> None:
        """The class constructor."""
        self.counter = 0

    def reset(self) -> None:
        """Restarts from the first color."""
        self.counter = 0

    def change(self) -> None:
        """Moves to the next color."""
        self.counter += 1

    def __call__(self) -> str:
        """Returns the current color."""
        return self.COLORS[self.counter % len(self.COLORS)]


# Global counter for the colors
current_color = ColorGetter()


def plot3D_init(figure):
    """
    Initialize the subplots needed to lhc plot with the given figure.

    Parameters
    ----------
    figure : TYPE Figure() of matplotlib

    """
    global ax_transversal, ax_longitudinal, fig
    fig = figure
    figure.clf()
    # Transversal subplot
    # set up the axes
    ax_transversal = figure.add_subplot(1, 2, 1, projection='3d')
    ax_transversal.set_xlabel('$X$')
    ax_transversal.set_ylabel('$Y$')
    ax_transversal.set_zlabel('$Z$')
    ax_transversal.set_xlim([-150, 150])
    ax_transversal.set_ylim([-150, 150])
    ax_transversal.set_zlim([-150, 150])
    ax_transversal.view_init(90, 270)

    # Longitudinal subplot
    # set up the axes
    ax_longitudinal = figure.add_subplot(1, 2, 2, projection='3d')
    ax_longitudinal.set_xlabel('$Z$')
    ax_longitudinal.set_ylabel('$Y$')
    ax_longitudinal.set_zlabel('$X$')
    ax_longitudinal.set_xlim([-300, 300])
    ax_longitudinal.set_ylim([-300, 300])
    ax_longitudinal.set_zlim([-300, 300])
    ax_longitudinal.view_init(90, 270)

    # Refresh plot to update changes
    figure.tight_layout()
    figure.canvas.draw()
    current_color.reset()


def plot_muontrack(track: ParticleTrack, energy=3) -> None:
    """
    Plots the track of a muon, using the energy parameter to extend the track
    outside the inner detector (muons pass all the detector layers).

    Parameters:
        track: The muon track to be displayed.
        energy: The default is 3.
    """
    current_color.change()
    color = current_color()
    ax_transversal.plot3D(
        [track.field13, track.field16 * energy],
        [track.field14, track.field17 * energy],
        [track.field15, track.field18 * energy],
        color,
    )
    ax_longitudinal.plot3D(
        [track.field15, track.field18 * energy],
        [track.field14, track.field17 * energy],
        [track.field13, track.field16 * energy],
        color,
    )

    # Refresh plot to update changes
    fig.tight_layout()
    fig.canvas.draw()


def plot_innertrack(track: ParticleTrack) -> None:
    """
    Plot the track of all particles except muons.

    Parameters
    ----------
    track_elements: TYPE list, contain the track elements
    """
    current_color.change()
    color = current_color()
    ax_transversal.plot3D(
        [track.field13, track.field16],
        [track.field14, track.field17],
        [track.field15, track.field18],
        color,
    )
    ax_longitudinal.plot3D(
        [track.field15, track.field18],
        [track.field14, track.field17],
        [track.field13, track.field16],
        color,
    )
    
    # Refresh plot to update changes
    fig.tight_layout()
    fig.canvas.draw()


def plot_cluster(phi: float, theta: float, eta: float, amplitude: float = 10) -> None:
    """Plots the cluster using an sphere.
    
    Phi, theta and eta indicate the position where the sphere has to be plotted.

    Parameters
    ----------
    phi: Phi value of the 3D sphere coordinates.
    theta: Theta value of the 3D sphere coordinates
    eta: Eta value of the 3D sphere coordinates.
    amplitude: The cluster energy.
    """
    if amplitude != 10:
        amplitude = amplitude * 10 + 2
    # Depending on eta value set the r coordinate, information proportionated
    # by WP5 team, REINFORCE project.
    if np.abs(eta) < 1.5:
        r = 150
    else:
        r = 210
    # Pass from sphere coordinates to cartesian coordinates
    x = r * np.sin(theta) * np.cos(phi)
    y = r * np.sin(theta) * np.sin(phi)
    z = r * np.cos(theta)
    # Make the sphere
    u = np.linspace(0, 2 * np.pi, 100)
    v = np.linspace(0, np.pi, 100)
    x = amplitude * np.outer(np.cos(u), np.sin(v)) + x
    y = amplitude * np.outer(np.sin(u), np.sin(v)) + y
    z = amplitude * np.outer(np.ones(np.size(u)), np.cos(v)) + z
    # Plot the sphere in the subplots
    ax_longitudinal.plot_surface(z, y, x, color='k')
    ax_transversal.plot_surface(x, y, z, color='k')
    # Refresh plot to update changes
    fig.tight_layout()
    fig.canvas.draw()
