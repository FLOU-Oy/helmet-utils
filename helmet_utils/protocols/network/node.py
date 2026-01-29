from typing import Protocol, Iterable, Any
from .link import LinkProtocol
from .network import NetworkProtocol
from .transitsegment import TransitSegmentProtocol
from .turn import TurnProtocol

class NodeProtocol(Protocol):
    id: str
    # The number as a string. Read-only.

    # The node number. The node number can be modified, and all links, turns and transit segments will be updated accordingly, but the new number must not already exist in the database.
    number: int

    # Boolean value indicating if this node is a centroid. Read-only.
    is_centroid: bool

    # Boolean value indicating if this node is an intersection. Read-only.
    # Set to True using Network.create_intersection and set to False using Network.delete_intersection.
    is_intersection: bool

    # The network to which the node belongs. Read-only.
    network: NetworkProtocol


    ## Standard attributes
    # The x-coordinate of the node.
    x: float

    # The y-coordinate of the node.
    y: float

    # Node user data item 1. Referred to as ‘ui1’ in procedure specifications.
    data1: float | None

    # Node user data item 2. Referred to as ‘ui2’ in procedure specifications.
    data2: float | None

    # Node user data item 3. Referred to as ‘ui3’ in procedure specifications.
    data3: float | None

    # Four-character label for the node.
    label: str | None


    ## Transit Result attributes
    # These attributes are only available if the scenario has valid transit results at the time of network creation, i.e. Scenario.has_transit_results is True.

    # The initial boardings result from the last transit assignment. Referred to as ‘inboa’ in procedure specifications and function expressions.
    initial_boardings: float | None

    # The final alightings result from the last transit assignment. Referred to as ‘fiali’ in procedure specifications and function expressions.
    final_alightings: float | None

    # See id.
    def __str__(self) -> str: ...

    # Return the link from the node with i_node_id to this node, or None if it does not exist.
    def incoming_link(self, i_node_id: str) -> LinkProtocol: ...

    # Return an iterator over all links with this node as the J-node.
    def incoming_links(self) -> Iterable[LinkProtocol]: ...

    # Return the link from the current node to the node with j_node_id, or None if it does not exist.
    def outgoing_link(self, j_node_id) -> LinkProtocol: ...

    # Return an iterator over all links with this node as the I-node.
    def outgoing_links(self) ->  Iterable[LinkProtocol]: ...

    # Return the turn with this node as the J-node and the I-node and K-node as identified i_node_id and k_node_id, or None if no such turn exists.
    def turn(self, i_node_id, k_node_id) -> TurnProtocol: ...

    # Return an iterator over all turns with this node as the J-node.
    def turns(self) -> Iterable[TurnProtocol]: ...

    # Return an iterator over all Transit Segments with this node as the J-node.
    def incoming_segments(self) -> Iterable[TransitSegmentProtocol]: ...

    # Return an iterator over all Transit Segments with this node as the I-node. If include_hidden is True hidden segments will also be included.
    def outgoing_segments(self, include_hidden=False) -> Iterable[TransitSegmentProtocol]: ...
    
    # node[name] may be used to access the extra attribute values from a node object, where name is the string name of the extra attribute; e.g. node["@nflag"]. This dictionary-like lookup works for any other attribute as well - including the Standard, Result, user-defined attributes and network fields.
    def __getitem__(self, key: str) -> Any: ...
