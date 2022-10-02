from bidder.visualize.api import VisualizeServiceApi
from bidder.visualize.service import VisualizeService
from bidder.store.bidder_store import BidderStore


class VisualizeServiceFactory:

    @classmethod
    def create(cls) -> VisualizeServiceApi:
        return VisualizeService(BidderStore())
