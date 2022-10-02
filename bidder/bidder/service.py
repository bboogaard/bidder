import random

from bidder.bidder.api import BidderAgentServiceApi
from bidder.bidder.models import BidIntention, CallRequest, CallResponse, EvaluateRequest


class BidderAgentService(BidderAgentServiceApi):

    def call(self, request: CallRequest) -> CallResponse:
        pass_after = random.choice(list(range(0, self.bidder.pass_after))) if self.bidder.pass_after else None
        if self.bidder.max_bid <= request.current_bid or (pass_after and request.bid_round > pass_after):
            return CallResponse(bidder=self.bidder, bid_intention=BidIntention.PASS)

        return CallResponse(
            bidder=self.bidder,
            bid_intention=BidIntention.BID,
            bid=min(request.current_bid + self.bidder.inc_bid, self.bidder.max_bid)
        )

    def evaluate(self, request: EvaluateRequest):
        if request.has_won:
            diff = self.bidder.max_bid - request.winning_bid
            self.bidder.max_bid = max(self.bidder.max_bid - diff, self.bidder.max_bid - self.bidder.dec_bid)
            child = self.bidder.clone()
            self.bidder_store.save_bidder(child)
        elif request.winning_bid > self.bidder.max_bid:
            diff = request.winning_bid - self.bidder.max_bid
            self.bidder.max_bid = min(self.bidder.max_bid + diff, self.bidder.max_bid + self.bidder.inc_bid)
        self.bidder_store.save_bidder(self.bidder)
