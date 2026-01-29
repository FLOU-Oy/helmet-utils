from typing import Protocol, Iterable, Any
from ...types import DomainType, ModeType
from .network import NetworkProtocol


class ModeProtocol(Protocol):
    # The one character ID of the mode.
    id: int

    # Changed in version 4.1.4: Property is now settable, and the related network elements will be updated, as long as the new ID value is not already in use.

    # The type of the mode. One of ‘AUTO’, ‘TRANSIT’, ‘AUX_AUTO’, or ‘AUX_TRANSIT’.
    type: ModeType

    # The network to which the mode belongs. Read-only.
    network: NetworkProtocol

    # Standard attributes

    # The description of the mode, up to 10 characters.
    description: str

    # The speed of the mode as a constant or a function of the form keyword*value.
    speed: int | str

    # Applicable only to modes of type ‘AUX_TRANSIT’. If specified in the expression form, the keyword must be one of “ul1”, “ul2”, “ul3” or “timau”.

    # Operating cost per unit length per vehicle (‘AUTO’) or per person (‘AUX_TRANSIT’), in the range 0.00 to 999.99.
    cost_dist_coeff: float | None

    # Applicable only to modes of type ‘AUTO’ and ‘AUX_TRANSIT’.

    # Operating cost per hour per vehicle (‘AUTO’) or per person (‘AUX_TRANSIT’), in the range 0.00 to 999.99.
    cost_time_coeff: float | None

    # Applicable only to modes of type ‘AUTO’ and ‘AUX_TRANSIT’.

    # Energy consumption per unit length per vehicle (‘AUTO’) or per person (‘AUX_TRANSIT’), in the range 0.00 to 999.99.
    energy_dist_coeff: float | None

    # Applicable only to modes of type ‘AUTO’ and ‘AUX_TRANSIT’.

    # Energy consumption per hour per vehicle (‘AUTO’) or per person (‘AUX_TRANSIT’), in the range 0.00 to 999.99.
    energy_time_coeff: float | None

    # Applicable only to modes of type ‘AUTO’ and ‘AUX_TRANSIT’.

    # Note mode[name] may be used to access the network field values from a turn object, where name is the string name of the network field; e.g. turn["#name"].
    # See id.
    def __getitem__(self, key: str) -> Any: ...
    def __str__(self) -> str: ...

