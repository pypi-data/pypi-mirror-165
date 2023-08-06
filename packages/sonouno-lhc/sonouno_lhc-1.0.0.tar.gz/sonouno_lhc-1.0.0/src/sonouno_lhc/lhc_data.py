#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 28 08:18:55 2022

@author: sonounoteam

This script open the file and apply specific transforms to it.
"""
from __future__ import annotations

import math
import typing
import matplotlib.pyplot as plt
from pathlib import Path

from matplotlib.figure import Figure

from sonounolib import Track as AudioTrack

from . import lhc_plot
from . import lhc_sonification
from .models import Cluster, Track, Subject

SECONDS_BETWEEN_ELEMENTS = 1


def sonify_subject(subject: Subject) -> tuple[AudioTrack, Figure]:
    """Sonify one dataset."""
    print()
    print(subject.id)
    print(len(subject.id) * '=')

    fig = plt.figure(figsize=plt.figaspect(0.5))
    lhc_plot.plot3D_init(fig)
    sonified_object_ids = set()

    sound = AudioTrack(max_amplitude='int16')
    sonified_ids = set()

    for index, track in enumerate(subject.tracks):
        if track.id not in sonified_object_ids:
            track_sound = sonify_track(
                sonified_ids, track, subject.tracks[index+1:], subject.clusters
            )
            sound.add_track(track_sound).add_blank(SECONDS_BETWEEN_ELEMENTS)

    for cluster in subject.clusters:
        if cluster.id not in sonified_ids:
            cluster_sound = sonify_cluster(cluster)
            sound.add_track(cluster_sound).add_blank(SECONDS_BETWEEN_ELEMENTS)

    return sound, fig


def sonify_track(
    sonified_ids: set[str], track: Track, other_tracks: list[Track], clusters: list[Cluster]
) -> AudioTrack:
    """
    This method allows to iterate through a given event ploting and sonifying
    the data provided.

    Parameters:
        sonified_ids: The tracks or clusters that have already been sonified.
        track: The particule track to be sonified.
        other_tracks: The other particule tracks that have not been yet sonified.
        clusters: The clusters to be sonified.
    """

    cluster_tosonify = []

    # Restore variables
    converted_photon = ' '
 
    if track.is_muon:
        # If the track is a muon plot it
        lhc_plot.plot_muontrack(track)
    else:
        # If the track is not a muon plot a simple track
        lhc_plot.plot_innertrack(track)

    # With each track calculate if it points out a cluster or not, if points a
    # cluster we will sonify the track and the cluster; and check if there
    # are a close track
    for cluster in clusters:
        # Search if the track points a cluster
        distance = math.sqrt(
            (track.phi - cluster.phi) ** 2 + (track.theta - cluster.theta) **2
        )
        if distance > 0.07:
            continue

        # If the track points to the cluster, plot it and include it
        # in the list to sonify.
        lhc_plot.plot_cluster(
            phi=track.phi,
            theta=track.theta,
            eta=track.eta,
            amplitude=cluster.energy / 100,
        )
        cluster_tosonify.append(cluster)

        # In addition, search if there is a close track
        for track2 in other_tracks:
            distance = math.sqrt((track.phi - track2.phi)**2 + (track.theta - track2.theta)**2)

            if (
                distance < 0.04
                and track.field1 != track2.field1
            ):
                # If a very close track exists, plot it and set the variable
                # to reproduce the converted photon sound
                if track2.id not in sonified_ids:
                    sonified_ids.add(track2.id)
                lhc_plot.plot_innertrack(track2)
                converted_photon = track2.id
                print(converted_photon)

    """
    Sonification part
    """
    if cluster_tosonify:
        sonified_ids.update(_.id for _ in cluster_tosonify)

        # The track point out a cluster
        if len(cluster_tosonify) > 1:
            # Arreglar el mensaje aqui
            print(
                f"Could a track points out to more than one cluster? "
                f"{', '.join(_.id for _ in cluster_tosonify)}")
 
        cluster = cluster_tosonify[0]

        if converted_photon == ' ':
            print(
                'Sonifying ' + track.id + ' and ' + cluster.id
            )
            if track.is_muon:
                # The element is a muon with cluster
                """
                1) bip: the beginning of the detector
                2) continuous sound during 2 seconds: the track in the inner detector
                3) a tone with different frequency: change from inner detector to red calorimeter
                4) sound corresponding to the cluster with the continuous sound of the track of the muon
                """
                # For the amplitude of the sound we use the transverse energy
                # supposing a range of [0;100], we devide the value by 100
                # to normalize it.
                sound = lhc_sonification.muontrack_with_cluster(
                    cluster.energy / 100
                )
            else:
                # The element is an electron
                """
                1) bip: the beginning of the detector
                2) continuous sound during 2 seconds: the track in the inner detector
                3) a tone with different frequency: change from inner detector to red calorimeter
                4) sound corresponding to the cluster
                """
                sound = lhc_sonification.singletrack_withcluster(
                    cluster.energy / 100
                )
        else:
            # The element is a converted photon
            """
            1) bip: the beginning of the detector
            2) two continuous sound during 2 seconds: the tracks in the inner detector
            3) a tone with different frequency: change from inner detector to red calorimeter
            4) sound corresponding to the cluster
            """
            print(f'Sonifying {track.id}, {converted_photon} and {cluster.id}')
            sound = lhc_sonification.doubletrack_withcluster(
                cluster.energy / 100
            )
    else:
        # The track doesn't point to a cluster
        """
        1) bip: the beginning of the detector
        2) continuous sound during 2 seconds: the track in the inner detector
        3) a tone with different frequency: change from inner detector to red calorimeter
        """
        print(f'Sonifying {track.id}')
        if track.is_muon:
            sound = lhc_sonification.doubletrack_only()
        else:
            sound = lhc_sonification.singletrack_only()

    return sound


def sonify_cluster(
    cluster: Cluster
) -> AudioTrack:
    """
    This method allows to iterate through a given event ploting and sonifying
    the data provided.

    Parameters:
        cluster: The cluster element.
        play_sound_status: If true, play the cluster sonification.
    """

    # Plot the cluster
    lhc_plot.plot_cluster(
        phi=cluster.phi,
        theta=cluster.theta,
        eta=cluster.eta,
        amplitude=cluster.energy / 100,
    )

    # Sonify the cluster
    """
    1) bip: the beginning of the detector
    2) silence during 2 seconds: there are no track in the inner detector
    3) a tone with different frequency: change from inner detector to red calorimeter
    4) sound corresponding to the cluster
    """
    print('Sonifying ' + cluster.id)
    return lhc_sonification.cluster_only(cluster.energy / 100)
