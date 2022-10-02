import uuid

from bidder.auction.api import AuctionServiceApi
from bidder.auction.service import AuctionService
from bidder.store.bidder_store import BidderStore


class AuctionServiceFactory:

    @classmethod
    def create(cls, session: uuid.UUID, start_bid: int) -> AuctionServiceApi:
        return AuctionService(session, start_bid, BidderStore())
