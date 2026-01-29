from typing import Literal


DomainType = Literal['MODE', 'TRANSIT_VEHICLE', 'NODE', 'LINK', 'TURN', 'TRANSIT_LINE', 'TRANSIT_SEGMENT']
ModeType = Literal['AUTO', 'TRANSIT', 'AUX_AUTO', 'AUX_TRANSIT']
NetworkElementsType = Literal['modes', 'transit_vehicles', 'centroids', 'regular_nodes', 'links', 'turns', 'turn_entries', 'transit_lines', 'transit_segments']
NetworkFieldDataTypes = Literal['BOOLEAN', 'INTEGER32', 'REAL', 'STRING']