from typing import Protocol, Iterable, Any
from .node import NodeProtocol
from .link import LinkProtocol

class ShortestPathTreeProtocol(Protocol):

    """
    This class provides a node-to-node shortest path tree computed using Network.shortest_path_tree. It cannot be constructed directly.
    ShortestPathTree provides methods for iterating over and querying costs and paths to all reachable nodes and links.
    
    """
    # Iterator over nodes that can be reached in the shortest path tree
    def reachable_nodes(self) -> Iterable[NodeProtocol] | None: ...

    # Iterator over links that can be reached in the shortest path tree
    def reachable_links(self) -> Iterable[LinkProtocol] | None: ...

    # Iterator over tuples of (Node, cost) for each reachable node
    def node_costs(self) -> Iterable[tuple[NodeProtocol, float]] | None: ...

    # Iterator over tuples of (Link, cost) for each reachable link
    def link_costs(self) -> Iterable[tuple[LinkProtocol, float]] | None: ...

    # The total cost of the path to node node_id, where node_id is an integer or a string.
    def cost_to_node(self, node_id: int | str) -> float | None: ...

    # The total cost of the path to link, where link is a link.
    def cost_to_link(self, link: LinkProtocol) -> float | None: ...

    # The path to node node_id as a list of link objects, where node_id is an integer or a string.
    def path_to_node(self, node_id: str | int) -> Iterable[LinkProtocol] | None: ...

    # The path that finishes using link, where link is a link, returned as a list of links.
    def path_to_link(self, link: LinkProtocol) -> Iterable[LinkProtocol] | None: ...

