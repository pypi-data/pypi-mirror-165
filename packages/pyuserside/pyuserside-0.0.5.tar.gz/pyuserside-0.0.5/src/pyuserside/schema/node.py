from dataclasses import dataclass
from datetime import datetime


@dataclass
class Coordinates:
    lat: float
    lon: float


@dataclass
class NodeData:
    id: int
    address_id: int
    date_add: datetime
    entrance: int
    level: int
    level_id: int
    parent_id: int
    is_planned: int
    location: str
    comment: str
    name: str
    type: int
    custom_icon_id: int
    number: int
    coordinates: Coordinates

    def __post_init__(self):
        if isinstance(self.date_add, str):
            self.date_add = datetime.strptime(self.date_add, '%Y-%m-%d %H:%M:%S')
        if isinstance(self.coordinates, dict):
            self.coordinates = Coordinates(**self.coordinates)
