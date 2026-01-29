from typing import Protocol, Iterable, Any
from .node import NodeProtocol
from .link import LinkProtocol
from .transitline import TransitLineProtocol
from .network import NetworkProtocol

class TransitSegmentProtocol(Protocol):
    # A unique string identifier of the transit segment’s line, link, and loop_index (if the loop index is greater than 1). This will be in the form: "line-i_node-j_node" for non-loop segments, and "line-i_node-j_node-loop_index" for loop segments. Read-only.
    id: str

    # The transit line that the segment belongs to. Read-only.
    line: TransitLineProtocol

    # The index number of the transit segment. Read-only.
    number: int

    # The I-node of the transit segment. Read-only.
    i_node: NodeProtocol

    # The J-node of the transit segment. If this segment is the ‘hidden’ segment, the j_node will be None. Read-only.
    j_node: NodeProtocol

    # Index number of the transit segment on its link. The number of times the segment’s link has been encountered in the itinerary, including the current segment. Segments which encounter a link for the first time will have a value of 1. Read-only.
    loop_index: int

    # The link with the same I-node and J-node. Also known as the link that the transit segment operates on. If this segment is the final ‘hidden’ segment, this value will be None. Read-only.
    link: LinkProtocol


    ## Standard attributes

    # Boolean value if alightings are permitted at the I-node of the segment. 
    # Note that the values of allow_alightings is the boolean inverse of the variable ‘noali’ used in the Desktop and procedure specifications.
    allow_alightings: bool

    # Boolean value if boardings are permitted at the I-node of the segment. 
    # Note that the values of allow_boardings is the boolean inverse of the variable ‘noboa’ used in the Desktop and procedure specifications.
    allow_boardings: bool

    # The time in minutes that the transit vehicle spends at the I-node of the transit segment. 
    # Normally specified as a constant value, but may specified as value per unit length in which case factor_dwell_time_by_length is also set to True.
    dwell_time: float | None

    # Boolean value indicating if the value of dwell_time should be multiplied by the link length to get the value of dwell time to be used in the assignment.
    factor_dwell_time_by_length: bool

    # The number of the function of type transit travel time used on this link. Referred to as ‘ttf’ in procedure specifications.
    transit_time_func: int

    # Transit segment user data item 1. Referred to as ‘us1’ in procedure specifications and function expressions.
    data1: float | None

    # Transit segment user data item 2. Referred to as ‘us2’ in procedure specifications and function expressions.
    data2: float | None

    # Transit segment user data item 3. Referred to as ‘us3’ in procedure specifications and function expressions.
    data3: float | None

    ## Transit Result attributes
    # These attributes are only available if the scenario has valid transit results at the time of network creation, i.e. Scenario.has_transit_results is True.

    # The transit boarding result at the I-node of the segment, from the last transit assignment. Referred to as ‘board’ in procedure specifications and function expressions.
    transit_boardings: float | None

    # The transit travel time, including dwell time, result from the last transit assignment. Referred to as ‘timtr’ in procedure specifications and function expressions.
    transit_time: float | None

    # The transit volume result from the last transit assignment. Referred to as ‘voltr’ in procedure specifications and function expressions.
    transit_volume: float | None

    # See id.
    def __str__(self) -> str: ...
    # Note transit_segment[name] may be used to access the extra attribute values from a transit segment object, where name is the string name of the extra attribute; e.g. transit_segment["@alit"]. This dictionary-like lookup works for any other attribute as well - including the Standard, Result, user-defined attributes and network fields.
    def __getitem__(self, key: str) -> Any: ...


