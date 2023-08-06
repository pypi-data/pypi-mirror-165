from __future__ import annotations

from dataclasses import dataclass


@dataclass
class ParticleTrack:
    """Class representing a particule track."""
    id: str
    field1: str
    field2: str
    field3: str
    phi: float
    theta: float
    eta: float
    field7: str
    field8: str
    field9: str
    field10: str
    is_muon: bool
    field12: str
    field13: float
    field14: float
    field15: float
    field16: float
    field17: float
    field18: float

    @classmethod
    def from_data(cls, line: str) -> 'ParticleTrack':
        id, f1, f2, f3, phi, theta, eta, f7, f8, f9, f10, is_muon, f12, f13, f14, f15, f16, f17, f18 = line.split()
        return ParticleTrack(
            id=id, field1=f1, field2=f2, field3=f3, phi=float(phi), theta=float(theta), eta=float(eta),
            field7=f7, field8=f8, field9=f9, field10=f10, is_muon=bool(int(is_muon)), field12=f12, field13=float(f13), field14=float(f14),
            field15=float(f15), field16=float(f16), field17=float(f17), field18=float(f18),
        )


@dataclass
class Cluster:
    """Class representing a particule cluster."""
    id: str
    field1: str
    field2: str
    energy: float
    phi: float
    theta: float
    eta: float
    field7: str
    field8: str
    field9: str
    field10: str
    field11: str
    field12: str
    field13: str
    field14: str
    field15: str
    field16: str
    field17: str
    field18: str

    @classmethod
    def from_data(cls, line: str) -> 'Cluster':
        id, f1, f2, energy, phi, theta, eta, f7, f8, f9, f10, f11, f12, f13, f14, f15, f16, f17, f18 = line.split()
        return Cluster(
            id=id, field1=f1, field2=f2, energy=float(energy), phi=float(phi), theta=float(theta), eta=float(eta),
            field7=f7, field8=f8, field9=f9, field10=f10, field11=f11, field12=f12, field13=f13, field14=f14,
            field15=f15, field16=f16, field17=f17, field18=f18,
        )


@dataclass
class Event:
    """Class representing a unit of work."""
    id: str
    description: str
    tracks: list[ParticleTrack]
    clusters: list[Cluster]
