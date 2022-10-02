import random

from bidder.auction.api import AuctionServiceApi
from bidder.auction.models import Auction, AuctionResponse
from bidder.bidder.factory import BidderAgentServiceFactory
from bidder.bidder.models import Bidder, BidIntention, CallRequest, EvaluateRequest
from bidder.models import Strategy


class AuctionService(AuctionServiceApi):

    def run(self) -> AuctionResponse:
        strategies = Strategy.objects.all()
        if not (bidders := self.bidder_store.load_bidders()):
            bidders = [Bidder.for_strategy(strategy) for strategy in strategies]
        agents = [
            BidderAgentServiceFactory.create(bidder)
            for bidder in bidders
        ]
        current_bid = self.start_bid
        current_bidder = None
        bid_round = 1
        while True:
            responses = list(filter(
                lambda r: r.bid_intention == BidIntention.BID,
                [agent.call(CallRequest(bid_round, current_bid)) for agent in agents]
            ))
            if not responses:
                break
            highest_bid = max([response.bid for response in responses])
            current_bidders = list(map(
                lambda r: r.bidder,
                filter(lambda r: r.bid == highest_bid, responses)
            ))
            current_bidder = random.choice(current_bidders)
            current_bid = highest_bid
            bid_round += 1
        for agent in agents:
            agent.evaluate(EvaluateRequest(
                has_won=current_bidder == agent.bidder,
                winning_bid=current_bid
            ))
        auction = Auction.create(
            session=self.session,
            start_bid=self.start_bid,
            bidders=[agent.bidder for agent in agents],
            winner=current_bidder,
            winning_bid=current_bid if current_bidder else None
        )
        self.bidder_store.save_auction(auction)
        return AuctionResponse(
            auction=auction,
            winner=current_bidder,
            winning_bid=current_bid if current_bidder else None
        )
