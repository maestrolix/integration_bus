from dataclasses import dataclass
from datetime import datetime


@dataclass
class Artist:
    id: int
    name: str
    albums: list['Album']
    rating: float


@dataclass
class Album:
    id: int
    title: str
    release_date: datetime
    compositions: list['Composition']
    rating: float


@dataclass
class Composition:
    id: int
    title: str
    rating: float
