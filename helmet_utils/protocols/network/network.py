from typing import Protocol, Iterable, Any
from ...types import DomainType, ModeType
from .mode import ModeProtocol
from .node import NodeProtocol
from .link import LinkProtocol
from .turn import TurnProtocol
from .transitline import TransitLineProtocol
from .transitsegment import TransitSegmentProtocol
from .transitvehicle import TransitVehicleProtocol

class NetworkProtocol(Protocol):
    # Valid modes: 'modes', 'transit_vehicles', 'centroids', 'regular_nodes', 'links', 'turns', 'turn_entries', 'transit_lines', and 'transit_segments'.
    element_totals: dict
    coord_unit_length: float

    # Support for the equals comparison operator == (i.e. network1 == network2).
    # Return True if other is a Network object with identical modes, nodes, links, turns, transit vehicles, transit lines, and transit segments, with identical attributes and values for all corresponding elements (elements with the same ID in both networks). Otherwise return False.
    def __eq__(self, other: object) -> bool: ...
    # Return a list of the names of attributes currently defined for network elements in domain type. 
    # Available values for type are: 'MODE', 'TRANSIT_VEHICLE', 'NODE', 'LINK', 'TURN', 'TRANSIT_LINE', and 'TRANSIT_SEGMENT'.
    def attributes(self, type: DomainType) -> Iterable[str]: ...
    
    # Create a new attribute on network elements of type with name and values initialized to default_value.
    # The name can be any string name of any length, providing flexibility in script implementation. 
    # However, in order for the attribute values to be stored on disk with Scenario.publish_network, 
    # an extra attribute or network field with the same name must exist in the Scenario.
    def create_attribute(self, type: DomainType, name: str, default_value=0) -> Any | None: ...

    # Change the name of the attribute old_name in domain type to new_name.
    def rename_attribute(self, type: DomainType, old_name: str, new_name: str) -> Any | None: ...
    
    # Copy the values of the attribute name in domain type to a new attribute new_name.
    def copy_attribute(self, type: DomainType, name: str, new_name: str) -> Any | None: ...

    # Delete the attribute in domain type specified by name.
    def delete_attribute(self, type: DomainType, name: str) -> None: ...


    ## Mode methods
    # Return the mode with the given id, or None if it does not exist.
    def mode(self, id: str) -> ModeProtocol | None: ...

    def modes(self) -> Iterable[ModeProtocol]: ...

    # The type must be one of ‘AUTO’, ‘TRANSIT’, ‘AUX_AUTO’, or ‘AUX_TRANSIT’.
    def create_mode(self, type: ModeType, id: str) -> ModeProtocol: ...

    # Delete the mode identified by id. See cascade delete.
    def delete_mode(self, id:str, cascade:bool=False) -> None: ...

    # Return the next available mode identifier (characters a-z, A-Z and 0-9) in alphanumeric order.
    def available_mode_identifier(self) -> str: ...


    ## Node methods
    def node(self, id:str) -> NodeProtocol | None: ... # Perhaps could reference NodeProtocol?

    def nodes(self) -> Iterable[NodeProtocol] | None: ...

    def centroids(self) -> Iterable[NodeProtocol] | None: ...

    def regular_nodes(self) -> Iterable[NodeProtocol] | None: ...

    def create_node(self, id: str, is_centroid:bool) -> NodeProtocol: ...

    def create_centroid(self, id: str) -> NodeProtocol: ...

    def create_regular_node(self, id: str) -> NodeProtocol: ...

    def delete_node(self, id: str, cascade:bool=False) -> None: ...

    def available_node_identifier(self, start_id:str=1) -> str: ...


    ## Link methods
    # Return the link connecting from the node specified by i_node_id to the node specified by j_node_id, or None if it does not exist.
    def link(self, i_node_id: str, j_node_id: str) -> LinkProtocol | None: ...

    # Return an iterator over all the links in the network.
    def links(self) -> Iterable[LinkProtocol] | None: ...

    # Create and return a new link from the node specified by i_node_id to the node specified by j_node_id with active modes, an iterable of mode objects or modes IDs.
    def create_link(self, i_node_id: str, j_node_id: str, modes: Iterable[ModeProtocol | str]) -> LinkProtocol: ...

    # Delete the link identified by i_node_id and j_node_id. See cascade delete.
    def delete_link(self, i_node_id: str, j_node_id: str, cascade:bool=False) -> None: ...

    # Split the link identified by i_node_id and j_node_id into two links, using new_node_id for the new intermediate node (must not already exist). 
    # If include_reverse is True the reverse link will also be split (if it exists). 
    # The link will be split at proportion along the link length from the i_node (between 0 and 1).
    # Return the newly created node.
    # The newly created links will have the same values for all attributes as the original link, 
    # with the exception of length, and vertices, which will be split according to the specified proportion. 
    # All turns adjacent to the link will be updated. Any transit segments on the link will also be split, 
    # and will have the same value for all attributes as the original segment.
    def split_link(self, i_node_id:str, j_node_id:str, new_node_id:str, include_reverse:bool=True, proportion: float=0.5) -> NodeProtocol: ...  # Could perhaps be NodeProtocol

    # Split the link identified by i_node_id and j_node_id into two links, at the location on the link closest to the position (x_pos, y_pos), using new_node_id for the new intermediate node (must not already exist).
    def split_link_at_location(self, i_node_id: str, j_node_id: str, new_node_id: str, x_pos:float, y_pos: float, include_reverse:bool=True) -> NodeProtocol: ...

    # Delete the node specified by node_id and merge the pairs of corresponding incoming / outgoing links and transit segments. 
    # The attribute values for the newly merged links will be taken from mapping if provided (with the exception of link modes); see merge_links_mapping(). 
    # Link modes for the newly merged links will correspond to all modes specified on the pairs of corresponding incoming / outgoing links.
    # Only nodes that are shape nodes can be merged. Raise an error if there are more than two nodes adjacent to this node, 
    # there are an unbalanced number of incoming and outgoing links, a transit line starts or ends at the node, or the node is a centroid or intersection.
    def merge_links(self, node_id: str, mapping: dict=None) -> None: ...

    # Return a dictionary of the default attribute values that would be used for the merged links and transit transit segments for node node_id. 
    # The dictionary contains two keys, “links” and “transit_segments”, which contain a dictionary mapping the pairs of network elements that will be merged to a dictionary of the default attribute values.
    # The default values for the attributes are taken from the first (incoming) network element, except for link length and vertices. 
    # Link length will be the sum of the length of the two links, and vertices will be the concatenation of the vertices of the two links.
    # Raise an error if the incoming and outgoing links cannot be merged. See merge_links().
    # The intended use is to provide a default attribute mapping which may be reviewed and modified prior to executing a link merge.
    def merge_links_mapping(self, node_id: str) -> dict: ...

    ## Turn methods
    # Return the turn at the node specified by j_node_id, from the node specified by i_node_id to the node specified by k_node_id, or None if it does not exist.
    def turn(self, i_node_id: str, j_node_id: str, k_node_id: str) -> TurnProtocol | None: ...  # Could perhaps be TurnProtocol?

    # Return an iterator over all the turns in the network.
    def turns(self) -> Iterable[TurnProtocol] | None: ...

    # Return an iterator over all the intersections (all nodes with is_intersection=True) in the network.
    def intersections(self) -> Iterable[NodeProtocol] | None: ...

    # Set is_intersection to True for the node specified by id and create the turns at the intersection.
    # Return the node specified by id.
    # Only regular nodes may become intersections (is_centroid = False). Upon initialization, U-turns are banned (assigned penalty_func = 0), and all other turns are unpenalized (assigned penalty_func = -1).
    def create_intersection(self, id: str) -> NodeProtocol: ...

    # Delete all turns at the intersection identified by the node id, and sets the node attribute is_intersection to False.
    def delete_intersection(self, id: str) -> None: ...


    ## Transit vehicle methods
    # Return the transit vehicle with the given id, or None if it does not exist.
    def transit_vehicle(self, id: str) -> TransitVehicleProtocol | None: ...

    # Return an iterator over all the transit vehicles in the network.
    def transit_vehicles(self) -> Iterable[TransitVehicleProtocol] | None: ...

    # Create and return a new transit vehicle with the given id and mode specified by mode_id.
    def create_transit_vehicle(self, id: str, mode_id: str) -> TransitVehicleProtocol: ...

    # Delete the transit vehicle identified by id. See cascade delete.
    def delete_transit_vehicle(self, id: str, cascade: bool=False) -> None: ...

    # Return the next available transit vehicle identifier.
    def available_transit_vehicle_identifier(self) -> str: ...


    ## Transit Line methods
    # Return the transit line with the given id, or None if it does not exist.
    def transit_line(self, id: str) -> TransitLineProtocol | None: ...  # Could perhaps be TransitLineProtocol?

    # Return an iterator over all the transit lines in the network.
    def transit_lines(self) -> Iterable[TransitLineProtocol] | None: ...

    # Return an iterator over all the transit segments in the network.
    def transit_segments(self) -> Iterable[TransitSegmentProtocol] | None: ...

    # Create and return a new transit line with id, transit vehicle specified by transit_vehicle_id and routed through the iterable of nodes specified by itinerary.
    # Itinerary is a iterable of two or more regular node IDs. There must be a link between each pair of adjacent nodes in the itinerary.
    def create_transit_line(self, id: str, transit_vehicle_id: str, itinerary: Iterable[str]) -> TransitLineProtocol: ...


    # Delete the transit line identified by id.
    def delete_transit_line(self, id: str) -> None: ...

    # Create and return a duplication of the transit line data and itinerary (including the transit segments data) for line source_id with the new id destination_id. The transit segment sequence will be reversed if reverse_itinerary is True.
    def copy_transit_line(self, source_id: str, destination_id: str, reverse_itinerary: bool=False) -> TransitLineProtocol: ...


    ## Shortest path
        # Build a shortest path tree and return a new shortest path tree object representing node-to-node shortest paths on the network.

        # origin_node_id: Source for the shortest path tree. Can be an id or a node instance. Can be the id of a regular node or a centroid.
        # link_costs: Link attribute containing the link costs to be used in the shortest path computation. Specified as a string using the Network API link attribute naming conventions. Eg “auto_time”, “length”, “@lcst”, etc…
        # excluded_links: A list of links to exclude when computing the shortest paths.
        # consider_turns: Whether to consider turn penalties/costs or not.
        # turn_costs: Turn attribute containing the turn costs to be used in the shortest path computation. None is equivalent to cost of 0 for permitted turns. Specified as a string using the Network API turn attribute naming conventions. Eg “auto_time”, “@pcst”, etc…
        # max_cost: The maximum allowed cost for any path, after which the tree stops expanding. Can have a substantial impact on run time.
    def shortest_path_tree(self, origin_node_id: str, link_costs: str, excluded_links:Iterable[str] | None = None, consider_turns:bool=True, turn_costs:str=None, max_cost:float=None) -> Any: ...


    ## Partial read/writes
    # Similar to Scenario.get_attribute_values but used to do a partial read of attribute values from this network. See Scenario.get_attribute_values for full details.
    def get_attribute_values(self, type: DomainType, names: Iterable[str]) -> Any | None: ...

    # Similar to Scenario.set_attribute_values but sets attribute values on this network. See Scenario.set_attribute_values for full details.
    def set_attribute_values(self, type: DomainType, names: Iterable[str], values: Iterable[Any]) -> Any | None: ...

    # If publishable is True, this network can be published back to disk using Scenario.publish_network.
    publishable: bool

