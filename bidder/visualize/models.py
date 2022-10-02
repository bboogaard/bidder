from dataclasses import dataclass

from bidder.models import Graph


@dataclass
class CreateLineGraphResponse:
    graph: Graph
