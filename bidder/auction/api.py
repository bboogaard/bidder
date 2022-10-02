import uuid
from abc import ABC

from bidder.auction.models import AuctionResponse
from bidder.store.bidder_store import BidderStore


class AuctionServiceApi(ABC):

    session: uuid.UUID

    start_bid: int

    bidder_store: BidderStore

    def __init__(self, session: uuid.UUID, start_bid: int, bidder_store: BidderStore):
        self.session = session
        self.start_bid = start_bid
        self.bidder_store = bidder_store

    def run(self) -> AuctionResponse:
        raise NotImplementedError()
