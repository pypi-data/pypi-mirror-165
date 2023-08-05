"""Describes a number of classes related to the compatibility graph."""
from __future__ import annotations

from collections import defaultdict
from itertools import combinations
from typing import Any, Union, Optional, Iterable

from kep_solver.entities import Donor, Recipient


class Vertex:
    """A vertex in a digraph representing a donor (directed or
    non-directed)."""

    def __init__(self, index: int, represents: Donor) -> None:
        self._index: int = index
        self._represents: Donor = represents
        self._properties: dict[str, Any] = {}
        self._edges_out: list[Edge] = []
        self._edges_in: list[Edge] = []

    @property
    def index(self) -> int:
        """Get the index (in the graph) of this vertex.

        :return: the index
        """
        return self._index

    def isNdd(self) -> bool:
        """True if this vertex corresponds to a non-directed donor.

        :return: True if this vertex corresponds to a non-directed
            donor
        """
        return self.donor.NDD

    @property
    def donor(self) -> Donor:
        """Return the donor associated with this vertex.

        :return: the associated donor"""
        return self._represents

    def addEdgeIn(self, edge: Edge) -> None:
        """Add an edge leading in to this vertex.

        :param edge: the edge
        """
        self._edges_in.append(edge)

    def addEdgeOut(self, edge: Edge) -> None:
        """Add an edge leading out from this vertex.

        :param edge: the edge
        """
        self._edges_out.append(edge)

    @property
    def edgesIn(self) -> list[Edge]:
        """Return the list of edges leading in to this vertex.

        :return: the list of edges leading in to this vertex.
        """
        return self._edges_in

    @property
    def edgesOut(self) -> list[Edge]:
        """Return the list of edges leading out from this vertex.

        :return: the list of edges leading out of this vertex.
        """
        return self._edges_out

    def adjacent(self) -> list[Vertex]:
        """Return the neighbours of this vertex

        :return: the list of neighbouring vertices
        """
        return [edge.end for edge in self.edgesOut]

    def __str__(self) -> str:
        """Return a string representation of the vertex."""
        if self.isNdd():
            return f"V({self.donor} ({self.index}))"
        else:
            return f"V({self.donor},{self.donor.recipient} ({self.index}))"

    def __repr__(self) -> str:
        return str(self)


class Exchange:
    """An exchange is either a cycle or a chain. This class lets us embed
    information (like embedded exchanges, or alternates) into the exchange.
    """

    def __init__(self, _id: str, vertices: list[Vertex]):
        self._id: str = _id
        self._vertices: tuple[Vertex, ...] = tuple(vertices)
        self._alternates: list[Exchange] = []
        self._embedded: list[Exchange] = []

    @property
    def id(self) -> str:
        """The ID of the exchange."""
        return self._id

    @property
    def vertices(self) -> tuple[Vertex, ...]:
        """The vertices in this exchange."""
        return self._vertices

    @property
    def chain(self) -> bool:
        """Returns True if this exchange represents a chain."""
        return self._vertices[0].isNdd()

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Exchange):
            return NotImplemented
        return self.id == other.id

    def __neq__(self, other: object) -> bool:
        return not (self == other)

    def __len__(self):
        """Returns the number of vertices (donors) in the exchange. Note that
        in the case of a non-directed altruistic donor, this will be greater
        than the number of recipients in the exchange.
        """
        return len(self._vertices)

    def __getitem__(self, index):
        """Gets the vertex at the appropriate index in the chain.

        :param index: The desired index
        """
        return self._vertices[index]

    def __iter__(self):
        """Allow iteration over exchanges, by returning an iterator to the
        vertices in it.
        """
        return self._vertices.__iter__()

    def __str__(self) -> str:
        return f"{self._vertices}"

    def __repr__(self) -> str:
        return str(self)

    def all_recipients(self) -> list[Recipient]:
        """Get all of the recipients."""
        return [v.donor.recipient for v in self._vertices if not v.isNdd()]

    def backarc_exchanges_uk(self) -> list[Exchange]:
        """Return the exchanges that contain backarcs from this exchange (by
        the UK definition of backarc).

        A backarc, by UK counting, is only defined for exchanges with three
        transplants (i.e., three donors). Let the three donors be A, B, and C.
        A backarc exists if A (respectively B and C) can donate to the paired
        recipient of C (respectively A and B).

        :return: A list containing each Exchange object that has a backarc from
            this Exchange.
        """
        if len(self) == 2:
            return []
        if len(self) != 3:
            raise Exception(
                "Backarcs are not defined for exchanges of length 4 or more"
            )
        backarc_exchanges = []
        for ind, v in enumerate(self):
            prev_v = self[(ind - 1) % len(self)]
            prev_donor = prev_v.donor
            donor = v.donor
            # Backarcs are tricky to deal with as if there is an NDD, we cannot
            # access its recipient.
            if prev_donor.NDD:
                # Need to find exchange containing backarc back to NDD
                recipients = set([donor.recipient])
            else:
                if donor.NDD:
                    # Need to find backarc from NDD to previous recipient
                    recipients = set([prev_donor.recipient])
                else:
                    # No NDDs involved, just look for exchange with same two
                    # recipents
                    recipients = set([donor.recipient, prev_donor.recipient])
            # Note that a backarc may exist in an alternate (rather than
            # embedded) exchange if this exchange is a chain, as an exchange is
            # an alternate if it has the same set of recipients (unlike
            # embedded exchanges, which have a strict subset only). This can
            # occur in a long chain, if there is also a two-way cycle between
            # the two vertices representing directed (paired) donors.
            if self.chain:
                for exchange in self.alternates:
                    # Backarc must have length 2
                    if len(exchange) != 2:
                        continue
                    if set(exchange.all_recipients()) == recipients:
                        backarc_exchanges.append(exchange)
                        break
            for exchange in self.embedded:
                if set(exchange.all_recipients()) == recipients:
                    backarc_exchanges.append(exchange)
                    break
        return backarc_exchanges

    def num_backarcs_uk(self) -> int:
        """Return the number of backarcs in this exchange (by the UK definition
        of backarc).

        A backarc, by UK counting, is only defined for exchanges with three
        transplants (i.e., three donors). Let the three donors be A, B, and C.
        A backarc exists if A (respectively B and C) can donate to the paired
        recipient of C (respectively A and B).

        :return: The number of backarcs in this Exchange.
        """
        return len(self.backarc_exchanges_uk())

    @property
    def alternates(self) -> list[Exchange]:
        """Return the alternate exchanges for this exchange. An alternate
        exchange is one that still matches exactly the same set of recipients,
        but possibly with either different donors (if some recipients are
        paired with multiple donors) or perhaps different donors and recipients
        are paired together.
        """
        return self._alternates

    def add_alternate(self, alt: Exchange) -> None:
        """Add an alternate exchange. An alternate exchange is one that still
        matches exactly the same set of recipients, but possibly with either
        different donors (if some recipients are paired with multiple donors)
        or perhaps different donors and recipients are paired together.

        :param alt: The alternate exchange.
        """
        if alt != self:
            self._alternates.append(alt)

    def add_alternates(self, alts: Iterable[Exchange]) -> None:
        """Add alternate exchanges. An alternate exchange is one that still
        matches exactly the same set of recipients, but possibly with either
        different donors (if some recipients are paired with multiple donors)
        or perhaps different donors and recipients are paired together.

        :param alts: The alternate exchanges.
        """
        for alt in alts:
            self.add_alternate(alt)

    @property
    def embedded(self) -> list[Exchange]:
        """Returns the exchanges embedded in this exchange. An embedded
        exchange is one that still matches some of the recipients within this
        exchange, but does not match any recipients not in this exchange.
        """
        return self._embedded

    def add_embedded(self, embed: Exchange) -> None:
        """Add an embedded exchange. An embedded exchange is one that still
        matches some of the recipients within this exchange, but does not match
        any recipients not in this exchange.

        :param embed: The embedded exchange.
        """
        self._embedded.append(embed)

    def add_embeddeds(self, embeds: Iterable[Exchange]) -> None:
        """Adds embedded exchanges. An embedded exchange is one that still
        matches some of the recipients within this exchange, but does not match
        any recipients not in this exchange.

        :param embeds: The embedded exchanges.
        """
        for embed in embeds:
            self.add_embedded(embed)

    def __hash__(self):
        return hash(tuple([v.index for v in self.vertices]))


class Edge:
    """An edge in a digraph, representing a potential transplant. An
    edge is always associated with a donor.
    """

    def __init__(self, donor: Donor, start: Vertex, end: Vertex) -> None:
        self._donor: Donor = donor
        self._properties: dict[str, Any] = {}
        self._start_vertex: Vertex = start
        self._end_vertex: Vertex = end

    def __repr__(self) -> str:
        return str(self)

    def __str__(self) -> str:
        return f"Edge({self._start_vertex} -> {self._end_vertex})"

    @property
    def donor(self) -> Donor:
        """Return the donor associated with this transplant.

        :return: The associated donor
        """
        return self._donor

    @property
    def end(self) -> Vertex:
        """Return the end-point of this edge.

        :return: the end Vertex of this edge
        """
        return self._end_vertex

    def addProperty(self, name: str, value) -> None:
        """Add an arbitrary property to this edge. This can be used
        for e.g. a score value associated with the transplant.

        :param name: the name of the property
        """
        self._properties[name] = value

    def getProperty(self, name: str) -> Any:
        """Get a property of this transplant.

        :param name: the name of the property
        :return: the associated value, which may have any type
        """
        return self._properties[name]


class CompatibilityGraph:
    """A digraph representing a KEP instance. Note that each vertex is
    a donor. Each edge corresponds to a potential transplant, and thus
    is associated with a donor that is paired with the recipient at
    beginning of the arc.
    """

    def __init__(self, instance=None):
        self._vertices: list[Vertex] = []
        self._edges: list[Edge] = []

        # Map each recipient or ndd to a vertex object
        self._vertex_map: dict[Union[Donor, Recipient], Vertex] = {}
        if instance is not None:
            for donor in instance.donors():
                self.addDonor(donor)
            for transplant in instance.transplants():
                self.addEdges(
                    transplant.donor,
                    transplant.recipient,
                    properties={"weight": transplant.weight},
                )

    @property
    def size(self) -> int:
        """The number of vertices in the graph.

        :return: the number of vertices
        """
        return len(self._vertices)

    @property
    def vertices(self) -> list[Vertex]:
        """The vertices in the graph.

        :return: the vertices
        """
        return self._vertices

    def edges(self) -> list[Edge]:
        """The edges in the graph.

        :return: the edges
        """
        return self._edges

    def addDonor(self, donor: Donor) -> None:
        """Add a vertex representing a donor.

        :param donor: a donor to be added to the graph.
        """
        vertex = Vertex(len(self._vertices), donor)
        self._vertices.append(vertex)
        self._vertex_map[donor] = vertex

    def donorVertex(self, donor: Donor) -> Vertex:
        """Get the vertex associated with a donor.

        :param donor: the donor to find
        :return: the vertex associated with the donor
        """
        return self._vertex_map[donor]

    def addEdges(self, donor: Donor, recip: Recipient, **properties: dict[str, Any]):
        """Add edges to the digraph corresponding to some potential
        transplant, optionally with some additional properties. Note
        that since the graph uses donors to represent vertices, if the
        given recipient has multiple donors then one edge will be added
        for each paired donor

        :param donor: the donor in the transplant
        :param recip: the recipient in the transplant
        :param properties: an optional dictionary mapping property
            names (as strings) to properties
        """
        start = self._vertex_map[donor]
        for pairedDonor in recip.donors():
            end = self._vertex_map[pairedDonor]
            edge = Edge(donor, start, end)
            for name, value in properties.items():
                edge.addProperty(name, value)
            start.addEdgeOut(edge)
            end.addEdgeIn(edge)
            self._edges.append(edge)

    def findChains(self, maxChainLength: int, index_offset: int = 0) -> list[Exchange]:
        """Finds and returns all chains in this graph. Note that this
        is specifically chains, and does not include cycles.

        :param maxchainLength: the maximum length of any chain
        :param index_offset: By default, chains are given IDs starting at zero. By
          setting this parameter to a non-zero value, IDs start at this number. This
          can help avoid ID clashes.
        :returns: a list of chains, where each chain is represented as
            a list of vertices
        """
        chains: list[Exchange] = []
        used = [False] * self.size
        stack: list[Vertex] = []

        def _extend(v: Vertex):
            chains.append(
                Exchange(f"{len(chains) + index_offset}", [vert for vert in stack])
            )
            if len(stack) == maxChainLength:
                return
            for w in v.adjacent():
                if not used[w.index]:
                    used[w.index] = True
                    stack.append(w)
                    _extend(w)
                    stack.pop()
                    used[w.index] = False

        for vert in self.vertices:
            if not vert.isNdd():
                continue
            used = [False] * self.size
            stack = [vert]
            _extend(vert)
        return chains

    def findCycles(self, maxCycleLength: int, index_offset: int = 0) -> list[Exchange]:
        """Finds and returns all cycles in this graph. Note that this
        is specifically cycles, and does not include chains.

        :param maxCycleLength: the maximum length of any cycle
        :param index_offset: By default, chains are given IDs starting at zero. By
          setting this parameter to a non-zero value, IDs start at this number. This
          can help avoid ID clashes.
        :returns: a list of cycles, where each cycle is represented as
        a list of vertices
        """
        # Implementing a variant of Johnson's algorithm from
        # Finding All The Elementary Circuits of a Directed Graph,
        # Donald B. Johnson, SIAM J.
        # Comput., 1975
        # There are some changes, however. Blocklists (B(n) in the
        # paper) aren't used, as since we limit cycle lengths we will
        # return when the stack is too long, but that doesn't mean we
        # must've created all cycles through a given vertex. For the
        # same reason, v is unblocked after each visit, regardless of
        # whether we find any cycles
        blocked: list[bool] = [False] * self.size
        stack: list[int] = []
        cycles: list[list[int]] = []

        def _unblock(u: int):
            blocked[u] = False

        def _circuit(v: int, component: list[int]) -> bool:
            flag = False
            if len(stack) == maxCycleLength:
                return False
            stack.append(v)
            blocked[v] = True
            for w in self.vertices[v].adjacent():
                if w.index not in component:
                    continue
                if w.index == s:
                    flag = True
                    cycles.append(list(stack + [s]))
                elif not blocked[w.index]:
                    if _circuit(w.index, component):
                        flag = True
            _unblock(v)
            stack.pop(-1)
            return flag

        s = 0

        def _tarjan(num_forbidden_vertices: int) -> Optional[list[int]]:
            index = 0
            component = None
            stack = list()
            indices = [-1] * self.size
            lowlink = [-1] * self.size
            onStack = [False] * self.size

            def _strongconnect(v: int, index: int) -> tuple[int, Optional[list[int]]]:
                indices[v] = index
                lowlink[v] = index
                index += 1
                onStack[v] = True
                component = None
                stack.append(v)
                for w in self.vertices[v].adjacent():
                    if w.index < num_forbidden_vertices:
                        continue
                    if indices[w.index] == -1:
                        index, component = _strongconnect(w.index, index)
                        lowlink[v] = min(lowlink[v], lowlink[w.index])
                    elif onStack[w.index]:
                        lowlink[v] = min(lowlink[v], indices[w.index])
                if lowlink[v] == indices[v]:
                    component = stack
                return index, component

            for v in range(num_forbidden_vertices, self.size):
                if indices[v] == -1:
                    index, component = _strongconnect(v, index)
                if component is not None:
                    return component
            return None

        while s < self.size:
            # Let Ak be adj matrix of strongly connected component K of
            # the induced graph on {s, s+1, ... , n} that contains the
            # lowest vertex
            component = _tarjan(s)
            if component is None:
                s = self.size
            else:
                s = component[0]
                for i in component:
                    blocked[i] = False
                _circuit(s, component)
                s += 1

        realCycles: list[Exchange] = []
        for indices in cycles:
            # Johnson's always adds the first vertex onto the end as
            # well, but we remove it
            real = [self.vertices[i] for i in indices[:-1]]
            realCycles.append(Exchange(f"{len(realCycles) + index_offset}", real))
        return realCycles


def build_alternates_and_embeds(exchanges: list[Exchange]) -> None:
    """Finds and adds alternate aned embedded exchanges based on the given exchanges. An
    alternate exchange is one that still matches exactly the same set of
    recipients, but possibly with either different donors (if some recipients
    are paired with multiple donors) or perhaps different donors and recipients
    are selected for transplant.  An embedded exchange is one that matches some
    (but not all) of the recipients within this exchange, but still does not
    match any recipients not in this exchange. Note that in both cases, if the
    exchange is a chain, we require that any alternate or embedded exchanges
    that are also chains must still be initiated by the same non-directed
    donor.

    :param exchanges: The exchanges to search for alternates
    """
    cache: dict[tuple[Recipient, ...], list[Exchange]] = defaultdict(list)
    # First create a mapping from sets of recipients to possible exchanges
    for exchange in exchanges:
        recipients = exchange.all_recipients()
        # Sort the recipients so we don't think [1,2] is different to [2,1]
        recipients.sort(key=lambda r: r.id)
        cache[tuple(recipients)].append(exchange)
    # Next, add the alternates to each exchange
    for exchange in exchanges:
        recipients = exchange.all_recipients()
        # Sort the recipients so we don't think [1,2] is different to [2,1]
        recipients.sort(key=lambda r: r.id)
        if exchange.chain:
            first = exchange[0].donor
            exchange.add_alternates(
                e
                for e in cache[tuple(recipients)]
                if not e.chain or e[0].donor == first
            )
        else:
            exchange.add_alternates(e for e in cache[tuple(recipients)] if not e.chain)
        # Note: We allow a chain consisting of only a non-directed donor, but
        # they should not be counted as an "embedded" exchange, hence minimum
        # size of 1 below
        for embed_size in range(1, len(recipients)):
            for subset in combinations(recipients, embed_size):
                # Recipients is already sorted, so subsets should be too
                if exchange.chain:
                    first = exchange[0].donor
                    exchange.add_embeddeds(
                        e
                        for e in cache[tuple(subset)]
                        if not e.chain or e[0].donor == first
                    )
                else:
                    exchange.add_embeddeds(
                        e for e in cache[tuple(subset)] if not e.chain
                    )
