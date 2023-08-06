"""Expose the node."""
import typing
import graphviz as _graphviz
from hornet import state as _state


class Node:
    """Represent a node."""

    def __init__(self, identity: str, attrs: dict = {}):
        """Put a node in a graph."""
        self.identity = identity
        self.digraph: _graphviz.Digraph = _state.get_digraph()
        self.digraph.node(self.identity, None, attrs)

    def __lt__(self, other: "Node" | typing.Iterable["Node"]) -> "Node":
        """Add an edge from `other` to `self`."""
        nodes = other
        if hasattr(other, "__iter__"):
            result = None
            nodes = other
        else:
            result = other
            nodes = [other]

        for node in nodes:
            self._select_inner(node).edge(node.identity, self.identity)

        return result

    def __gt__(self, other: "Node") -> "Node":
        """Add an edge from `self` to `other`."""
        nodes = other
        if hasattr(other, "__iter__"):
            result = None
            nodes = other
        else:
            result = other
            nodes = [other]

        for node in nodes:
            self._select_inner(node).edge(
                self.identity,
                node.identity,
            )
        return result

    def __sub__(self, other: "Node") -> "Node":
        """Implement - ."""
        self._select_inner(other).edge(
            self.identity,
            other.identity,
            None,
            arrowhead="none",
            arrowtail="none",
        )
        return other

    def _select_inner(self, other: "None") -> _graphviz.Digraph:
        """Return the `inner` digraph of `self` or `other`."""
        return _state.select_inner(self.digraph, other.digraph)
