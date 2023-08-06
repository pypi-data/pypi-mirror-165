from __future__ import annotations

from typing import Iterator

from .models import Subject, Track, Cluster

SEPARATOR = '---------'


def extract_subjects(lines: list[str]) -> Iterator[Subject]:
    """Iterates through the data, one subject at a time."""
    extracted_lines = []
    for line in lines:
        if SEPARATOR in line:
            if not extracted_lines:
                continue
            yield convert_subject(extracted_lines)
            extracted_lines = []
        else:
            extracted_lines.append(line)


def convert_subject(lines: list[str]) -> Subject:
    """Converts data lines into a Subject instance."""
    id_ = lines[0]
    description = lines[1]
    tracks = []
    clusters = []
    for line in lines[2:]:
        if line.startswith('track'):
            tracks.append(Track.from_data(line))
        elif line.startswith('cluster'):
            clusters.append(Cluster.from_data(line))
        else:
            raise
    subject = Subject(id=id_, description=description, tracks=tracks, clusters=clusters)
    return subject

