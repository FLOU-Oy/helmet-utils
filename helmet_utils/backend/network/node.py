from typing import Iterable, Any

from .network import ExportedNetwork
from .turn import ExportedTurn
from .link import ExportedLink
from .transitsegment import ExportedTransitSegment

class ExportedNode:
    def __init__(
        self,
        *,
        number: int,
        network: ExportedNetwork,
        x: float,
        y: float,
        data1: float | None,
        data2: float | None,
        data3: float | None,
        label: str | None,
        is_centroid: bool = False,
        is_intersection: bool = False,
        ):
        self.number = number
        self.network = network
        self.x = x
        self.y = y

        self.is_centroid = is_centroid
        self.is_intersection = is_intersection
        self.label = label

        # User data
        self.data1: float | None = data1
        self.data2: float | None = data2
        self.data3: float | None = data3

        # Transit results
        self.initial_boardings: float | None = None
        self.final_alightings: float | None = None

    # ---- Derived / read-only properties ----

    @property
    def id(self) -> str:
        return str(self.number)

    def __str__(self) -> str:
        return self.id

    # ---- Link access ----

    def incoming_link(self, i_node_id: str) -> ExportedLink | None:
        i = int(i_node_id)
        return self.network.links.get((i, self.number))

    def incoming_links(self) -> Iterable[ExportedLink]:
        for (i, j), link in self.network.links.items():
            if j == self.number:
                yield link

    def outgoing_link(self, j_node_id: str) -> ExportedLink | None:
        j = int(j_node_id)
        return self.network.links.get((self.number, j))

    def outgoing_links(self) -> Iterable[ExportedLink]:
        for (i, j), link in self.network.links.items():
            if i == self.number:
                yield link

    # ---- Turns ----

    def turn(self, i_node_id: str, k_node_id: str) -> ExportedTurn | None:
        return self.network.turns.get(
            (int(i_node_id), self.number, int(k_node_id))
        )

    def turns(self) -> Iterable[ExportedTurn]:
        for (_, j, _), turn in self.network.turns.items():
            if j == self.number:
                yield turn

    # ---- Transit segments ----

    def incoming_segments(self) -> Iterable[ExportedTransitSegment]:
        for seg in self.network.transit_segments:
            if seg.j_node == self.number:
                yield seg

    def outgoing_segments(self, include_hidden=False) -> Iterable[ExportedTransitSegment]:
        for seg in self.network.transit_segments:
            if seg.i_node == self.number:
                if include_hidden or not seg.hidden:
                    yield seg

    # ---- Attribute lookup ----

    def __getitem__(self, key: str) -> Any:
        # Works for "@nflag", standard fields, etc.
        return getattr(self, key)
    