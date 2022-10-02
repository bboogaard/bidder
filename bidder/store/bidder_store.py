import uuid
from typing import Dict, List, Optional

from django.conf import settings
from redis import connection, Redis

from bidder.auction.models import Auction
from bidder.bidder.models import Bidder


connection_pool = connection.ConnectionPool(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=settings.REDIS_DB)


class BidderStore:

    connection: Redis

    AUCTION_SET = 'auctions'

    BIDDER_SET = 'bidders'

    def __init__(self):
        self.connection = Redis(connection_pool=connection_pool)

    def save_auction(self, auction: Auction):
        self.connection.hset(str(auction.id), mapping=auction.serialize())
        self.connection.sadd(self.AUCTION_SET, str(auction.id))

    def load_auction(self, auction_id: uuid.UUID) -> Optional[Auction]:
        data = self.connection.hgetall(str(auction_id))
        return Auction.load(self._decode_data(data)) if data else None

    def load_auctions(self, session: Optional[uuid.UUID] = None) -> List[Auction]:
        result = []
        for auction_id in self.connection.smembers(self.AUCTION_SET):
            if (auction := self.load_auction(uuid.UUID(auction_id.decode()))) and (
                    not session or session == auction.session):
                result.append(auction)
        return result

    def save_bidder(self, bidder: Bidder):
        self.connection.hset(str(bidder.id), mapping=bidder.serialize())
        self.connection.sadd(self.BIDDER_SET, str(bidder.id))

    def load_bidder(self, bidder_id: uuid.UUID) -> Optional[Bidder]:
        data = self.connection.hgetall(str(bidder_id))
        return Bidder.load(self._decode_data(data)) if data else None

    def load_bidders(self) -> List[Bidder]:
        result = []
        for bidder_id in self.connection.smembers(self.BIDDER_SET):
            if bidder := self.load_bidder(uuid.UUID(bidder_id.decode())):
                result.append(bidder)
        return result

    @staticmethod
    def _decode_data(data: Dict) -> Dict:
        return {
            key.decode(): value.decode()
            for key, value in data.items()
        }
