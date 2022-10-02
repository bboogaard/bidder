import uuid
from dataclasses import dataclass
from typing import Set

from django.core.management import BaseCommand

from bidder.auction.factory import AuctionServiceFactory


@dataclass
class Winner:
    times_won: int
    agents: Set[uuid.UUID]


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('start_bid', type=int, nargs=1)
        parser.add_argument('runs', type=int, nargs='?', default=1)

    def handle(self, *args, **options):
        session = uuid.uuid4()
        print('Running auctions...')
        responses = []
        for _ in range(options['runs']):
            responses.append(AuctionServiceFactory.create(session, options['start_bid'][0]).run())
        print(f'Run {len(responses)} auctions')
        print('Bidder\t\tTimes won\t\tAgents')
        winners = {}
        for response in responses:
            if not (winner := response.winner):
                continue
            if not (saved_winner := winners.get(winner.identifier)):
                saved_winner = Winner(times_won=0, agents=set())
                winners[winner.identifier] = saved_winner
            saved_winner.times_won += 1
            saved_winner.agents.add(winner.id)
        for identifier, winner in sorted(winners.items(), key=lambda w: w[1].times_won):
            print(f'{identifier}\t\t{winner.times_won}\t\t{len(winner.agents)}')
