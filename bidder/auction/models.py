import time
import uuid
from dataclasses import asdict, dataclass
from typing import Dict, List, Optional

from bidder.bidder.models import Bidder


@dataclass
class Auction:
    id: uuid.UUID
    session: uuid.UUID
    created: int
    start_bid: int
    bidders: List[uuid.UUID]
    winner: Optional[uuid.UUID] = None
    winning_bid: Optional[int] = None

    @classmethod
    def create(cls, session: uuid.UUID, start_bid: int, bidders: List[Bidder], winner: Optional[Bidder] = None,
               winning_bid: Optional[int] = None):
        return cls(
            id=uuid.uuid4(),
            session=session,
            created=int(time.time()),
            start_bid=start_bid,
            bidders=[bidder.id for bidder in bidders],
            winner=winner.id if winner else None,
            winning_bid=winning_bid
        )

    @classmethod
    def load(cls, data: Dict[str, str]) -> 'Auction':
        return cls(
            id=uuid.UUID(data['id']),
            session=uuid.UUID(data['session']),
            created=int(data['created']),
            start_bid=int(data['start_bid']),
            bidders=[uuid.UUID(bidder_id) for bidder_id in data['bidders'].split(',')],
            winner=uuid.UUID(data['winner']) if data['winner'] else None,
            winning_bid=int(data['winning_bid']) if data['winning_bid'] else None
        )

    def serialize(self):
        result = asdict(self)
        result['id'] = str(result['id'])
        result['session'] = str(result['session'])
        result['winner'] = str(result['winner']) if result['winner'] else None
        result['bidders'] = ','.join([str(bidder) for bidder in result['bidders']])
        return result


@dataclass
class AuctionResponse:
    auction: Auction
    winner: Optional[Bidder] = None
    winning_bid: Optional[int] = None
