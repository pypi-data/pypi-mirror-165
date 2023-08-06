"""Expose the root class to draw diggraphs."""
import os.path
import graphviz as _graphviz
import hornet.state as _state


class Digraph:
    """Represent a digraph.

    Call the constructor at the top of `with` block.

    """

    def __init__(
        self, filepath: str, graph_attrs: dict[str, str], cleanup=False
    ):
        """Define digraph attributes."""
        self._filepath = filepath
        self._cleanup = cleanup
        self._graph_attrs = graph_attrs
        name, extension = os.path.splitext(self._filepath)
        if extension == "":
            raise RuntimeError(f"Add an extension to {self._filepath}")

        self.digraph: _graphviz.Digraph = _graphviz.Digraph(
            filename=f"{name}.gv",
            format=extension[1:],
            graph_attr=self._graph_attrs,
        )

    def has(self, digraph: _graphviz.Digraph):
        """Return true if it holds `digraph`."""
        return self.digraph is digraph

    def __enter__(self):
        """Declare a graph."""
        _state.put_diggraph(self)

    def __exit__(self, exc_type, exc_value, traceback):
        """Render the digraph."""
        # https://graphviz.readthedocs.io/en/stable/api.html#graphviz.Graph.render
        self.digraph.render(cleanup=self._cleanup, outfile=self._filepath)
        _state.remove_digraph(self)


class SubGraph:
    """Represent a subgraph."""

    def __init__(self, graph_attrs: dict[str, str] = dict()):
        """Use this constructor with `with` block."""
        self.digraph = _graphviz.Digraph(graph_attr=graph_attrs)

    def __enter__(self):
        """Declare a subgraph."""
        _state.put_subgraph(self)

    def __exit__(self, exc_type, exc_value, traceback):
        """Add itself to the parent graph."""
        _state.remove_subgraph(self)
        parent = _state.get_inner_graph()
        parent.subgraph(self.digraph)

    def has(self, digraph: _graphviz.Digraph):
        """Return true if it holds `digraph`."""
        return self.digraph is digraph


class Cluster:
    """Represent a cluster."""

    def __init__(self, graph_attrs: dict[str, str] = dict()):
        """Use this constructor with `with` block."""
        name = f"cluster_{_state.generate_cluster_id()}"
        self.digraph = _graphviz.Digraph(name=name, graph_attr=graph_attrs)

    def __enter__(self):
        """Declare a subgraph."""
        _state.put_subgraph(self)

    def __exit__(self, exc_type, exc_value, traceback):
        """Add itself to the parent graph."""
        _state.remove_subgraph(self)
        parent = _state.get_inner_graph()
        parent.subgraph(self.digraph)

    def has(self, digraph: _graphviz.Digraph):
        """Return true if it holds `digraph`."""
        return self.digraph is digraph
