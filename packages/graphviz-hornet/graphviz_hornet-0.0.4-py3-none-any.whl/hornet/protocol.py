"""Define protocols."""
import typing
from graphviz import Digraph


class NodeProtocol(typing.Protocol):
    """Interface of a node."""

    @property
    def identity(self) -> str:
        """ID of a node."""


class SubGraphProtocol(typing.Protocol):
    """Represent a subgraph."""

    @property
    def identity(
        self,
    ) -> str:
        """Identity."""


class DigGraphProtocol(typing.Protocol):
    """Represent a digraph."""
