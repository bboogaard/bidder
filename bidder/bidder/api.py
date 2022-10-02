from abc import ABC

from bidder.bidder.models import Bidder, CallRequest, CallResponse, EvaluateRequest
from bidder.store.bidder_store import BidderStore


class BidderAgentServiceApi(ABC):

    bidder: Bidder

    bidder_store: BidderStore

    def __init__(self, bidder: Bidder, bidder_store: BidderStore):
        self.bidder = bidder
        self.bidder_store = bidder_store

    def call(self, request: CallRequest) -> CallResponse:
        raise NotImplementedError()

    def evaluate(self, request: EvaluateRequest):
        raise NotImplementedError()
