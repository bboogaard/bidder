import random
import uuid
from dataclasses import asdict, dataclass, replace
from enum import Enum
from typing import Dict, Optional

from bidder.models import Strategy


@dataclass
class Bidder:
    id: uuid.UUID
    max_bid: int
    inc_bid: int
    dec_bid: int
    pass_after: Optional[int]

    @property
    def identifier(self):
        return '-'.join(map(str, [self.max_bid, self.inc_bid, self.dec_bid, self.pass_after]))

    @classmethod
    def for_strategy(cls, strategy: Strategy):
        return cls(
            id=uuid.uuid4(),
            max_bid=strategy.max_bid,
            inc_bid=strategy.inc_bid,
            dec_bid=strategy.dec_bid,
            pass_after=strategy.pass_after
        )

    @classmethod
    def load(cls, data: Dict[str, str]) -> 'Bidder':
        return cls(
            id=uuid.UUID(data['id']),
            max_bid=int(data['max_bid']),
            inc_bid=int(data['inc_bid']),
            dec_bid=int(data['dec_bid']),
            pass_after=int(data['pass_after']) if data['pass_after'] else None
        )

    def serialize(self):
        result = asdict(self)
        result['id'] = str(result['id'])
        result['pass_after'] = result['pass_after'] or ''
        return result

    def clone(self):
        return replace(self, **dict(
            id=uuid.uuid4(),
            max_bid=self.max_bid,
            inc_bid=self.copy(self.inc_bid),
            dec_bid=self.copy(self.dec_bid),
            pass_after=self.copy(self.pass_after)
        ))

    @staticmethod
    def copy(value: Optional[int]) -> Optional[int]:
        mutate = random.choice([True, False])
        return max(value + random.randint(-3, 3), 1) if value and mutate else value


class BidIntention(Enum):
    BID = 'bid'
    PASS = 'pass'


@dataclass
class CallRequest:
    bid_round: int
    current_bid: int


@dataclass
class CallResponse:
    bidder: Bidder
    bid_intention: BidIntention
    bid: Optional[int] = None


@dataclass
class EvaluateRequest:
    has_won: bool
    winning_bid: Optional[int] = None
