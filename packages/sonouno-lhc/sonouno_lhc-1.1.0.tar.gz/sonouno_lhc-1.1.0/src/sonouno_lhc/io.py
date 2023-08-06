"""Convert HYPATIA events from text format to an Event model.

Events are separated by: ---------------------------------

For each event, the following information are kept:

- Line 1: EventID

- Line 2: Missing ET | φ of Missing ET | Date & time | Event Number | Run Number | irrelevant number | irrelevant number | irrelevant number

- Tracks/Clusters section (starts from line 3 and ends right before the "Hits" word).
  There is one line per track in the inner detector or cluster in the electromagnetic calorimeter.
  The columns are common for both cases:
  name | charge | p | pT | φ | θ | η | cot(θ) | true kind | interest level | xmin (cm) | ymin (cm) | zmin (cm) | xmax (cm) | ymax (cm) | zmax (cm)

  "true kind" is based on simulation truth information: 0 (unknown), 1 (muon track), 2 (electron track), 3 (electron cluster), 4 (photon), 5 (converted photon)
  "interest level": is not important for this stage
  xmin, xmax etc.: are the coordinates of the first and last hit of a track in the inner detector (0 for clusters)

- The Hits section is not used (empty)

- "Clusters" section (actually provides details about the constituent hits of each above cluster).
  The columns are:
  ET | φ | θ | cluster_name | true kind

  "cluster name" is there so we know to which cluster each hit belongs

- Tiles section (hits in the hadronic calorimeter) may not be useful for this stage.
  The columns are:
  Tile ID | ET (GeV) | φ | θ

- The remaining sections (RPC, TGC, MDT, CSC) are not used.
"""

from __future__ import annotations

from typing import Iterator

from .models import Event, ParticleTrack, Cluster

SEPARATOR = '---------'


def extract_events(lines: list[str]) -> Iterator[Event]:
    """Iterates through the data, one event at a time."""
    extracted_lines = []
    for line in lines:
        if SEPARATOR in line:
            if not extracted_lines:
                continue
            yield convert_event(extracted_lines)
            extracted_lines = []
        else:
            extracted_lines.append(line)


def convert_event(lines: list[str]) -> Event:
    """Converts data lines into an Event instance."""
    id_ = lines[0]
    description = lines[1]
    tracks = []
    clusters = []
    for line in lines[2:]:
        if line.startswith('track'):
            tracks.append(ParticleTrack.from_data(line))
        elif line.startswith('cluster'):
            clusters.append(Cluster.from_data(line))
        else:
            raise
    event = Event(id=id_, description=description, tracks=tracks, clusters=clusters)
    return event

