"""Handling of KEP pools, which are just the rules, procedures and
algorithms for a particular KEP.
"""

from time import thread_time
from typing import Optional

from kep_solver.entities import Instance
from kep_solver.model import Objective, Model, CycleAndChainModel
from kep_solver.graph import Exchange


class ModelledExchange:
    """An exchange as modelled, including its value for various
    objectives and any other relevant information.
    """

    def __init__(self, exchange: Exchange, values: list[float]):
        """Constructor for ModelledExchange. Contains the Exchange object, and
        also the value of this exchange for the various objectives in this
        model.

        :param exchange: The exchange
        :param values: The value of this exchange for each objective
        """
        self._exchange = exchange
        self._values = values

    @property
    def exchange(self) -> Exchange:
        """The underlying exchange."""
        return self._exchange

    @property
    def values(self) -> list[float]:
        """The values of this exchange."""
        return self._values

    def __str__(self) -> str:
        """A human-readable representation of this exchange."""
        return str(self._exchange)


class Solution:
    """A solution to one instance of a KEP. Contains the exchanges, and
    the set of objective values attained.
    """

    def __init__(
        self,
        exchanges: list[ModelledExchange],
        scores: list[float],
        possible: list[ModelledExchange],
        times: list[tuple[str, float]],
    ):
        """Constructor for Solution. This class essentially just stores
        any information that may be useful.

        :param exchanges: the list of selected exchanges
        :param scores: the list of scores achieved for each objective
        :param possible: the set of possible exchanges, and their
            values for each objective
        :param times: The time taken for various operations. Each is a
            tuple with a string description of the action, and the time
            (in seconds)
        """
        self._selected: list[ModelledExchange] = exchanges
        self._values: list[float] = scores
        self._possible: list[ModelledExchange] = possible
        self._times: list[tuple[str, float]] = times

    @property
    def times(self) -> list[tuple[str, float]]:
        """Get the time taken for various operations. Each element of
        the returned list is a tuple where the first item is a string
        description of some operation, and the second item is the time
        taken in seconds.

        :return: the list of times (and their descriptions)
        """
        return self._times

    @property
    def selected(self) -> list[ModelledExchange]:
        """Get the selected solution.

        :return: the list of exchanges selected.
        """
        return self._selected

    @property
    def values(self) -> list[float]:
        """Get the Objective values of the selected solution.

        :return: the list of objective values
        """
        return self._values

    @property
    def possible(self) -> list[ModelledExchange]:
        """Return a list of all the possible chains and cycles that may
        be selected as ModelledExchange objects that contain the value of said
        exchange for each objective.

        :return: a list of cycles/chains as ModelledExchange objects
        """
        return self._possible


class Pool:
    """A KEP pool."""

    def __init__(
        self,
        objectives: list[Objective],
        maxCycleLength: int,
        maxChainLength: int,
        description: str,
    ):
        """Constructor for Pool. This represents a set of objectives, and
        parameters for running matchings (such as maximum cycle and chain
        lengths).

        :param objectives: the list of objectives
        :param maxCycleLength: The longest cycle length allowed.
        :param maxChainLength: The longest chain length allowed. Note that the
            length of a chain includes the non-directed donor.
        :param description: A description of this pool.
        """
        # Create a copy of the list of objectives with the magic colon
        self._objectives: list[Objective] = objectives[:]
        self._maxCycleLength: int = maxCycleLength
        self._maxChainLength: int = maxChainLength
        self._description: str = description

    @property
    def description(self) -> str:
        """A description of this pool."""
        return self._description

    @description.setter
    def description(self, desc) -> None:
        """A description of this pool."""
        self._description = desc

    @property
    def objectives(self) -> list[Objective]:
        """The list of objectives for this Pool."""
        return self._objectives

    @property
    def maxCycleLength(self) -> int:
        """The maximum length of cycles in this pool."""
        return self._maxCycleLength

    @property
    def maxChainLength(self) -> int:
        """The maximum length of chains in this pool. Note that this includes
        the non-directed donor, so a chain of length 1 only has a non-directed
        donor and no recipients."""
        return self._maxCycleLength

    def solve_single(
        self,
        instance: Instance,
        maxCycleLength: Optional[int] = None,
        maxChainLength: Optional[int] = None,
    ) -> tuple[Optional[Solution], Model]:
        """Run a single instance through this pool, returning the solution, or
        None if no solution is found (e.g., if the solver crashes).

        :param instance: The instance to solve
        :param maxCycleLength: The longest cycle allowed. If not specified, we
            use the default from the Pool
        :param maxChainLength: The longest chain allowed. If not specified, we
            use the default from the Pool
        :return: A tuple containing a Solution object, or None if an error
            occured, as well as the model that was solved.
        """
        if maxCycleLength is None:
            maxCycleLength = self._maxCycleLength
        if maxChainLength is None:
            maxChainLength = self._maxChainLength
        t = thread_time()
        model = CycleAndChainModel(
            instance,
            self._objectives,
            maxChainLength=maxChainLength,
            maxCycleLength=maxCycleLength,
        )
        times = [("Model building", thread_time() - t)]
        t = thread_time()
        solution: list[Exchange] = model.solve()
        times.append(("Model solving", thread_time() - t))
        if solution is None:
            return None
        values = model.objective_values
        exchange_values: dict[Exchange, list[float]] = {
            exchange: model.exchange_values(exchange) for exchange in model.exchanges
        }
        solutions = [ModelledExchange(ex, exchange_values[ex]) for ex in solution]
        possible = [
            ModelledExchange(ex, exchange_values[ex]) for ex in exchange_values.keys()
        ]
        return Solution(solutions, values, possible, times), model
