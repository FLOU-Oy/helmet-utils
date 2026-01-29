from typing import Protocol, Iterable, Any
from .link import LinkProtocol
from .network import NetworkProtocol

class TurnProtocol(Protocol):
    # A string representation of the I-, J- and K-nodes of the turn.: the I-node ID, J-node ID and K-node ID concatenated by dashes. Read-only.
    id: str

    # The I-node of the turn. Read-only.
    i_node: int

    # The J-node of the turn. Read-only.
    j_node: int

    # The K-node of the turn. Read-only.
    k_node: int

    # The link that this turn is coming from. Read-only.
    from_link: LinkProtocol

    # The link with this turn is going to. Read-only.
    to_link: LinkProtocol

    # The network to which the turn belongs. Read-only.
    network: NetworkProtocol


    ## Standard attributes

    # The number of the function of type ‘TURN_PENALTY’ used on this link. Referred to as ‘tpf’ in procedure specifications.
    penalty_func: int | None

    # Turn user data item 1. Referred to as ‘up1’ in procedure specifications and function expressions.
    data1: float | None

    # Turn user data item 2. Referred to as ‘up2’ in procedure specifications and function expressions.
    data2: float | None

    # Turn user data item 3. Referred to as ‘up3’ in procedure specifications and function expressions.
    data3: float | None

    ## Traffic Result attributes
    # These attributes are only available if the scenario has valid traffic results at the time of network creation, i.e. Scenario.has_traffic_results is True.

    # The auto volume result from the last traffic assignment. Referred to as ‘pvolau’ in procedure specifications and function expressions.
    auto_volume: float | None

    # The additional auto volume result from the last traffic assignment. Referred to as ‘pvolad’ in procedure specifications and function expressions.
    additional_volume: float | None

    # The auto travel time result from the last traffic assignment. Referred to as ‘ptimau’ in procedure specifications and function expressions.
    auto_time: float | None

    # See id.
    def __str__(seld) -> str: ...
    def __getitem__(self, key: str) -> Any: ...



