from typing import Iterable

from shapely import Point
from ..protocols.network.node import NodeProtocol
from ..protocols.network.link import LinkProtocol
from ..protocols.network.network import NetworkProtocol
from ..protocols.network.turn import TurnProtocol
from ..protocols.network.transitsegment import TransitSegmentProtocol

class Node:
    """
    Used to add functionality to Emme API or helmet_utils nodes

    """
    def __init__(self, backend: NodeProtocol):
        # Comes from either an active EMME project or an imported folder
        self._backend = backend

    # ---- Default attributes and properties ----

    @property
    def network(self) -> NetworkProtocol:
        return self._backend.network

    @property
    def id(self) -> str:
        return str(self._backend.id)
    
    @property
    def number(self) -> int:
        return self._backend.number
    
    @number.setter
    def number(self, value: int):
        self._backend.number = value
    
    @property
    def x(self) -> float:
        return self._backend.x
    
    @property
    def y(self) -> float:
        return self._backend.y
    
    @property
    def is_centroid(self) -> bool:
        return self._backend.is_centroid

    @property
    def is_intersection(self) -> bool:
        return self._backend.is_intersection

    @property
    def data_1(self) -> float:
        return self._backend.data1

    @property
    def data_2(self) -> float:
        return self._backend.data2
    
    @property
    def data_1(self) -> float:
        return self._backend.data3
    
    @property
    def label(self) -> str:
        return self._backend.label

    @property
    def final_alightings(self) -> float | None:
        return self._backend.final_alightings
    
    @property
    def initial_boardings(self) -> float | None:
        return self._backend.initial_boardings
    
    def incoming_link(self, i_node) -> LinkProtocol | None:
        return self._backend.incoming_link(i_node)

    def incoming_links(self) -> Iterable[LinkProtocol]:
        return self._backend.incoming_links()

    def outgoing_link(self, j_node) -> LinkProtocol | None:
        return self._backend.outgoing_link(j_node)

    def outgoing_links(self) -> Iterable[LinkProtocol]:
        return self._backend.outgoing_links()

    def turns(self) -> Iterable[TurnProtocol]:
        return self._backend.turns()

    def incoming_segments(self) -> Iterable[TransitSegmentProtocol]:
        return self._backend.incoming_segments()

    def outgoing_segments(self, include_hidden=False) -> Iterable[TransitSegmentProtocol]:
        return self. _backend.outgoing_segments(include_hidden=include_hidden)

    def __getitem__(self, key: str):
        return self._backend[key]

    def __setitem__(self, key: str, value):
        self._backend[key] = value

    def __getattr__(self, name):
        return getattr(self._backend, name)
    
    # ---- New properties ----
    
    @property
    def geometry(self) -> Point:
        return Point(self.x, self.y)
    
    # ---- New methods ----
