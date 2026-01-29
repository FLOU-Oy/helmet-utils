from typing import Protocol, Iterable, Any
from .mode import ModeProtocol
from .transitvehicle import TransitVehicleProtocol
from .network import NetworkProtocol
from .node import NodeProtocol
from .transitsegment import TransitSegmentProtocol

class TransitLineProtocol(Protocol):
    # The ID of this transit line. Up to 40 characters. The ID can contain any character, with the following exceptions:
    # Space (space), comma (,) and colon (:) are reserved characters which are used as delimiters to separate fields in transaction file formats.
    # To use a reserved character inside the transit line name field, enclose the entire string in single-quotes (‘).
    # Transit line names cannot by empty. A space is accepted as a transit line name.
    # Transit line names can have a leading space but trailing spaces are removed.
    id: str

    # The mode that the transit vehicle of this line uses. Read-only
    mode: ModeProtocol

    # The transit vehicle that this transit line uses. 
    # This property may be changed directly by assigning a new vehicle or valid vehicle id, 
    # if the mode of the new transit vehicle is available on all links on which the transit line operates.
    vehicle: TransitVehicleProtocol

    # The network to which the tranist line belongs. Read-only.
    network: NetworkProtocol


    ## Standard attributes

    # The description of the transit line, up to 120 characters. The description can contain any character. 
    # Spaces are allowed. A single-quote character (‘) is permitted as long as it is not followed by a separator (, : space).
    description: str

    # The average interval between the arrival of two consecutive vehicles in minutes. In the range 0.01 to 999.99
    headway: float

    # The default average speed in length units per hour. Used for the transit-only links that the line passes through, 
    # or when the transit travel time function on the segment is 0, 
    # or when the transit travel time function depends on the auto time and the traffic assignment is not available.
    speed: float 

    # The time in minutes of the layover at the last transit segment. In the range 0 to 999.99. 
    # Note: intermediate layovers are not supported via the Network API.
    layover_time: float

    # Transit line user data item 1. Referred to as ‘ut1’ in procedure specifications and function expressions.
    data1: float | None

    # Transit line user data item 2. Referred to as ‘ut2’ in procedure specifications and function expressions.
    data2: float | None

    # Transit line user data item 3. Referred to as ‘ut3’ in procedure specifications and function expressions.
    data3: float | None

    # See id.
    def __str__(self) -> str: ...
    
    # transit_line[name] may be used to access the extra attribute values from a transit line object, 
    # where name is the string name of the extra attribute; e.g. transit_line["@lgrpi"]. 
    # This dictionary-like lookup works for any other attribute as well - 
    # including the Standard, Result, user-defined attributes and network fields.
    def __getitem__(self, key: str) -> Any: ...


    # Return an iterator over the nodes that this transit line passes through.
    def itinerary() -> Iterable[NodeProtocol]: ...

    # Return the transit segment specified by id, where id is the index of the transit segment. 
    # The id may be specified as a positive number to count from the beginning of the transit line starting at 0, 
    # or as a negative number to count from the end of the transit line starting at -1, (the hidden segment).
    def segment(id: str) -> TransitSegmentProtocol: ...

    # Return an iterator over the transit segments on the line; 
    # include_hidden indicates if the final ‘hidden’ segment should be included.
    def segments(include_hidden:bool=False) -> Iterable[TransitSegmentProtocol]: ...
