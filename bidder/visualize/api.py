from abc import ABC

from bidder.visualize.models import CreateLineGraphResponse
from bidder.store.bidder_store import BidderStore


class VisualizeServiceApi(ABC):

    bidder_store: BidderStore

    def __init__(self, bidder_store: BidderStore):
        self.bidder_store = bidder_store

    def create_line_graph(self) -> CreateLineGraphResponse:
        raise NotImplementedError()
