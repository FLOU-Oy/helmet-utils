from typing import Protocol, Iterable, Any
from .mode import ModeProtocol
from .network import NetworkProtocol

class TransitVehicleProtocol(Protocol):
    # String version of the vehicle number. Read-only.
    id: str

    # The number of the vehicle.
    # Property is now settable, and the related network elements will be updated, 
    # as long as the new number value is not already in use.
    number: int

    # The mode that the vehicle uses. Must be of type ‘TRANSIT’.
    mode: ModeProtocol

    # The network to which the vehicle belongs. Read-only.
    network: NetworkProtocol


    ## Standard attributes

    # The description of the vehicle, up to 10 characters.
    description: str

    # The passenger car equivalent or unit (pce or pcu) of each transit vehicle, in the range 0.00 to 999.99.
    auto_equivalent: float

    # The number of seats per vehicle, in the range 1 to 999999.
    seated_capacity: int

    # The total number of passengers (seated + standing) the vehicle can accommodate, in the range 1 to 999999. The total_capacity must be equal to or greater than the seated_capacity.
    total_capacity: int

    # The number of vehicles of this type, in the range 1 to 999999.
    fleet_size: int

    # Operating cost per unit length travelled by vehicle, in the range 0.00 to 999.99.
    cost_dist_coeff: float

    # Operating cost per hour of vehicle operation, in the range 0.00 to 999.99.
    cost_time_coeff: float

    # Energy consumption per unit length travelled by vehicle, in the range 0.00 to 999.99.
    energy_dist_coeff: float

    # Energy consumption per hour of vehicle operation, in the range 0.00 to 999.99.
    energy_time_coeff: float

    # See id.
    def __str__(self) -> str: ...
    
    # transitvehicle[name] may be used to access the network field values from a transit vehicle object,
    #  where name is the string name of the network field; e.g. transitvehicle["#name"].
    def __getitem__(self, key: str) -> Any: ...

