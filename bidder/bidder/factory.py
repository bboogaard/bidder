from bidder.bidder.api import BidderAgentServiceApi
from bidder.bidder.service import BidderAgentService
from bidder.bidder.models import Bidder
from bidder.store.bidder_store import BidderStore


class BidderAgentServiceFactory:

    @classmethod
    def create(cls, bidder: Bidder) -> BidderAgentServiceApi:
        return BidderAgentService(bidder, BidderStore())
