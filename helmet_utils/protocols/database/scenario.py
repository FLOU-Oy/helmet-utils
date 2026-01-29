from typing import Protocol, Iterable, Any
from datetime import datetime

from ...types import DomainType, ModeType, NetworkElementsType, NetworkFieldDataTypes
from ..network import NetworkProtocol

class ScenarioProtocol(Protocol):
    # The scenario number as a string. Read-only.
    id: str

    # The scenario number. Read-only.
    number: int

    # The title of the scenario, up to 60 characters long.
    title: str

    # A dictionary of the number of network elements currently defined. Read-only. Valid keys are: 'modes', 'transit_vehicles', 'centroids', 'regular_nodes', 'links', 'turns', 'turn_entries', 'transit_lines', and 'transit_segments'.
    element_totals: dict[NetworkElementsType]

    # Boolean value indicating if the scenario has valid traffic assignment results.
    has_traffic_results: bool

    # The time and date (Python datetime object) of the last completed traffic assignment. Read-only.
    traffic_assignment_timestamp: datetime

    # The type of the last completed traffic assignment if the scenario has valid traffic results, or None if there are no traffic results. Read-only.
    traffic_assignment_type: Any | None

    # Boolean value indicating if the scenario has valid transit assignment results.
    has_transit_results: bool

    # The time and date (Python datetime object) of the last completed transit assignment. Read-only.
    transit_assignment_timestamp: datetime

    # The type of the last completed transit assignment if the scenario has valid transit results, or None if there are no transit results. Read-only.
    transit_assignment_type: Any | None

    # Boolean value indicating if the scenario is protected against modification.
    modify_protected: bool

    # Boolean value indicating if the scenario is protected against deletion.
    delete_protected: bool

    # The emmebank to which the scenario belongs. Read-only.
    emmebank: Any

    # A list of all the zone numbers (centroid ids) defined in the scenario, in ascending order. Read-only.
    zone_numbers: Iterable[int | str]

    # See id.
    def __str__(self) -> str: ...

    # See number.
    def __int__(self) -> int: ...

    # Return a list of the names of attributes currently defined for network elements in domain type. Available values for type are: 'MODE', 'TRANSIT_VEHICLE', 'NODE', 'LINK', 'TURN', 'TRANSIT_LINE', or 'TRANSIT_SEGMENT'.
    def attributes(self, type) -> Iterable[str]: ...

    # Return the extra attribute with the given id, or None if it does not exist.
    def extra_attribute(self, id) -> Any | None: ...

    # Return an iterator over all the extra attributes in the scenario.
    def extra_attributes(self) -> Iterable[Any] | None: ...

    # Return a new extra attribute with the given id for network domain type. The extra attribute values are initially set to default_value.
    # The type can be one of 'MODE', 'TRANSIT_VEHICLE', 'NODE', 'LINK', 'TURN', 'TRANSIT_LINE', or 'TRANSIT_SEGMENT'. The id can be up to 19 characters long with no spaces plus the first character '@'.
    def create_extra_attribute(self, type: DomainType, id: str, default_value: int=0) -> Any: ...

    # Delete the extra attribute specified by id.
    def delete_extra_attribute(self, id: str) -> None: ...

    # Create a new Network Field of the specified Network element type, data store atype, with id and description. The id must be unique for the element type, and it can be any length with no spaces and the first character '#'.
    # The type can be one of 'MODE', 'TRANSIT_VEHICLE', 'NODE', 'LINK', 'TURN', 'TRANSIT_LINE', or 'TRANSIT_SEGMENT'.

    # The atype can be one of 'BOOLEAN', 'INTEGER32', 'REAL', or 'STRING'.
    def create_network_field(self, type: DomainType, id: str, atype: NetworkFieldDataTypes, description: str='') -> Any: ...

    # Return the Network Field with the given id, and network element type, or None if it does not exist.
    def network_field(self, type: DomainType, id: str) -> Any | None: ...

    # Return an iterator over all the Network Fields in the scenario.
    def network_fields(self) -> Iterable[Any] | None: ...

    # Delete the network field specified by type and id.
    def delete_network_field(self, type, id) -> None: ...

    # Return a network which is an in-memory copy of the scenario network on disk. See The Network API for documentation of the available functionality.
    # Note The network object is separate from the network stored on disk in the scenario. Changes made to a network object are saved only after calling Scenario.publish_network.
    def get_network(self) -> NetworkProtocol: ...

    # Return a network with a partial load of selected element types and attribute values. This method is similar to get_network but returns only partial network topology of a network on disk with limited access to elements and attributes. This is useful in suitable applications to minimize memory consumption and load time. See also The Network API.
    # The element_types is a list of one or more network domain types from the EMME network hierarchy. Available values are 'MODE', 'TRANSIT_VEHICLE', 'NODE', 'LINK', 'TURN', 'TRANSIT_LINE', and 'TRANSIT_SEGMENT'. Specifying a higher-level domain will automatically bring required dependencies in the network hierarchy (e.g. specifying 'LINK' will also read in 'NODE' and 'MODE').
    # If include_attributes is True the attributes values will also be loaded in the network for the specified network domain types in element_types. If include_attributes is False no attributes values will be loaded. The attributes will always be available on the network elements, but if the values are not loaded, the values for all elements will be set to the default value.
    # If only certain attribute values are needed, they can be explicitly loaded using use Scenario.get_attribute_values followed by Network.set_attribute_values as needed.
    # Note that the network from get_partial_network does not include link shape: the property Link.vertices will be empty.
    # Note Because partial networks do not contain all network elements and attributes, care must be taken when publishing to a scenario on disk to avoid overwriting missing elements and attributes. As a safeguard, Network.publishable is set to False for partial networks. If you want to publish to a scenario using Scenario.publish_network, you must first set Network.publishable to True.
    def get_partial_network(self, element_types: Iterable[DomainType], include_attributes: bool) -> NetworkProtocol: ...

    # Replaces the scenario network on disk with the network in memory, mapping the domain attributes in the network to the domain attributes available in the scenario. The network on disk is completely replaced by the published network.
    # Note publish_network writes attribute data only; it does not add or remove extra attributes or network fields, nor does it change their description or default value.
    # If resolve_attributes is False, an error will be raised if the network contains attributes which are not defined in the scenario, or if the network does not contain attributes that are defined in the scenario.

    # If resolve_attributes is True, attributes that are defined in the network and do not exist in the scenario are ignored, and attributes that are defined in the scenario and do not exist in the network are set to the default value.

    # The presence of result attributes must match (as well as the Extra attributes and Network fields). Using publish_network does not remove or add the transit or traffic assignment results. It is up to the user to set the status appropriately using:

    # scenario.has_traffic_results = False
    # scenario.has_transit_results = False
    # However, the EMME prompt assignment status (output of the sta command) is erased after a call to publish_network. If the assignments have been run via Modeller tools then the full assignment status can be obtained from the Scenario status tool.

    # See also The Network API.
    # See also The methods get_attribute_values() and set_attribute_values(): these can be used to copy just certain attributes from the in-memory network to the scenario.
    # Note in order for a network to be published, Network.publishable must be True.
    def publish_network(self, network: NetworkProtocol, resolve_attributes:bool=False) -> None : ...

        
    # Used to do a partial read of attribute values from a scenario. This is useful in applications where:
    # Only certain attribute values need be updated in a currently constructed network, for instance after running other procedures which modify the database. Or,
    # Only certain attributes need to be loaded on a partial network, ie. after a call to get_partial_network.
    # Returns a data structure that must be passed to either:

    # Network.set_attribute_values, in which case the attributes are then available on the network for access/processing. Or,
    # Scenario.set_attribute_values to write attribute values to disk.
    # type: a network domain type, available values are 'MODE', 'TRANSIT_VEHICLE', 'NODE', 'LINK', 'TURN', 'TRANSIT_LINE', and 'TRANSIT_SEGMENT'.

    # names: a list of one or more attribute names on the domain of type, ie. the Standard, Result, and user-defined Extra Attributes and Network Fields of the corresponding network domain.

    # Note: an equivalent function is available for Network objects: Network.get_attribute_values.
    def get_attribute_values(self, type: DomainType, names: Iterable[str]) -> Any | None: ...


    # Used to do a partial write of attribute values to a scenario. The values parameter should be the object returned from a corresponding get_attribute_values call.
    # Note The get/set_attribute_values can be used between two scenarios, two networks, and between a scenario and a network.
    # For example, the following writes transit segment attributes data1 and transit_time_func from an in-memory network back to a scenario:
    #   elem_type = "TRANSIT_SEGMENT"
    #   attributes = ["data1", "transit_time_func"]
    #   values = network.get_attribute_values(elem_type, attributes)
    #   scenario.set_attribute_values(elem_type, attributes, values)
    # If a get/set_attribute_values is used between two scenarios or networks that don’t have the same topology for the given domain type, then only the values for those objects with identifiers that are common between both will be copied.
    def set_attribute_values(self, type: DomainType, names: Iterable[str], values: Iterable[Any]) -> Any | None: ...
