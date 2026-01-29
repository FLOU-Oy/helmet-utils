from typing import Protocol, Iterable, Any, Self
from .network import NetworkProtocol
from .turn import TurnProtocol
from .transitsegment import TransitSegmentProtocol

class LinkProtocol(Protocol):
    # A string representation of the I- and J-nodes of the link: the I-node ID and J-node ID concatenated by a dash. Read-only.
    id: str

    # The I-node of the link. Read-only.
    i_node: int

    # The J-node of the link. Read-only.
    j_node: int

    # The link with this link’s I-node as J-node, and J-node as I-node, or None if it does not exist. Read-only.
    reverse_link: Self | None

    # The list of the coordinate pairs of the intermediate vertices on the link. It is of the form: [(vertex_1.x, vertex_1.y), (vertex_2.x, vertex_2.y), ... ]
    # The vertices can no longer be changed in place. Instead, set link.vertices = vertices_list to update the values.

    # For example:
    #   vertices_list = link.vertices
    #   link.vertices = vertices_list
    #   vertices_list.append((633150.0, 5527521.0))
    vertices: Iterable[tuple[float, float]]
    
    # The list of the coordinate pairs of the vertices on the link, including the i_node and j_node coordinates. It is of the form: [(i_node.x, i_node.y), (vertex_1.x, vertex_1.y), ... (j_node.x, j_node.y)]
    shape: Iterable[tuple[float, float]]
    
    # The total length of the link through the intermediate vertices, using Network.coord_unit_length as a conversion factor.
    shape_length: float

    # A frozenset of the active modes on this link.
    # One technique to add modes to a link is to use the in-place set union operator: '|='. 
    # Or, to delete modes from a link use the in-place set difference operator: '-='. 
    # The modes to be modified must be contained in a Set or FrozenSet. 
    # For example, to add the mode ‘b’ to the current link, use: link.modes |= set([network.mode('b')])
    modes: frozenset

    # The network to which the link belongs. Read-only.
    network: NetworkProtocol


    ## Standard attributes

    # The link length.
    length: float

    # Integer indicating link type or classification, in the range 1 to 999.
    type: int

    # Number of lanes on the link, in the range 0.0 to 9.9. Referred to as ‘lanes’ in procedure specifications and function expressions.
    num_lanes: float

    # The number of the function of type ‘VOLUME_DELAY’ used on this link. Referred to as ‘vdf’ in procedure specifications.
    volume_delay_func: int

    # Link user data item 1. Referred to as ‘ul1’ in procedure specifications and function expressions.
    data1: float | None

    # Link user data item 2. Referred to as ‘ul2’ in procedure specifications and function expressions.
    data2: float | None

    # Link user data item 3. Referred to as ‘ul3’ in procedure specifications and function expressions.
    data3: float | None


    ## Traffic Result attributes
    # These attributes are only available if the scenario has valid traffic results at the time of network creation, i.e. Scenario.has_traffic_results is True.

    # The auto volume result from the last traffic assignment. Referred to as ‘volau’ in procedure specifications and function expressions.
    auto_volume: float | None

    # The additional auto volume result from the last traffic assignment. Referred to as ‘volad’ in procedure specifications and function expressions.
    additional_volume: float | None

    # The auto travel time result from the last traffic assignment. Referred to as ‘timau’ in procedure specifications and function expressions.
    auto_time: float | None

    ## Transit Result attribute
    # This attribute is only available if the scenario has valid transit results at the time of network creation, i.e. Scenario.has_transit_results is True.

    # The auxilary transit volume result from the last transit assignment. Referred to as ‘volax’ in procedure specifications and function expressions.
    aux_transit_volume: float | None

    # See id.
    def __str__(self) -> str: ...

    # link[name] may be used to access the extra attribute values from a link object, 
    # where name is the string name of the extra attribute; e.g. link["@lacap"]. 
    # This dictionary-like lookup works for any other attribute as well - 
    # including the Standard, Result, user-defined attributes and network fields.
    def __getitem__(self, key: str) -> Any: ...

    # Return an iterator over the turns with this link’s I-node and J-node as J-node and K-node respectively.
    def incoming_turns(self) -> Iterable[TurnProtocol]: ...

    # Return an iterator over the turns with this link’s I-node and J-node as I-node and J-node respectively.
    def outgoing_turns(self) -> Iterable[TurnProtocol]: ...

    # Return an iterator over the transit segments with this link’s I-node and J-node.
    def segments(self) -> Iterable[TransitSegmentProtocol]: ...


