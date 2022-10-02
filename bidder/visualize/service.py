import time
from collections import defaultdict
from io import BytesIO
from typing import Dict, List, Optional

import matplotlib.pyplot as plt
from django.core.files.images import ImageFile

from bidder.bidder.models import Bidder
from bidder.models import AgentProfile, Graph
from bidder.visualize.api import VisualizeServiceApi
from bidder.visualize.models import CreateLineGraphResponse


class VisualizeService(VisualizeServiceApi):

    def create_line_graph(self) -> CreateLineGraphResponse:
        totals = defaultdict(list)
        buffer = defaultdict(int)

        profiles = list(AgentProfile.objects.all())
        time_indices = []

        def _add_totals(idx):
            time_indices.append(idx)
            for prof in profiles:
                totals[prof.name].append(buffer[prof.name])

        bidders = self._get_bidders()

        for time_index, auction_bidders in enumerate(bidders):

            if time_index % 10 == 0:
                _add_totals(time_index)
                buffer = defaultdict(int)

            profile_data = self._get_profile_data(profiles, auction_bidders)
            for profile in profiles:
                buffer[profile.name] += profile_data[profile.name]

        _add_totals(len(bidders) - 1)

        for profile in profiles:
            plt.plot(time_indices, totals[profile.name], label=profile.name)
        plt.legend()
        fh = BytesIO()
        plt.savefig(fh)
        filename = str(int(time.time())) + '.png'
        graph = Graph()
        graph.image.save(filename, ImageFile(fh))
        return CreateLineGraphResponse(graph=graph)

    def _get_bidders(self) -> List[List[Bidder]]:
        bidders = []
        for auction in self.bidder_store.load_auctions():
            auction_bidders = []
            for bidder_id in auction.bidders:
                if bidder := self.bidder_store.load_bidder(bidder_id):
                    auction_bidders.append(bidder)
            bidders.append(auction_bidders)
        return bidders

    @staticmethod
    def _get_profile_data(profiles: List[AgentProfile], auction_bidders: List[Bidder]) -> Dict:

        def _meets_condition(limits: Optional[List[int]] = None, actual: Optional[int] = None) -> bool:
            return actual and (not limits or (limits[0] <= actual <= limits[1]))

        result = defaultdict(int)
        for bidder in auction_bidders:
            for profile in profiles:
                if all([
                    _meets_condition(profile.max_bid, bidder.max_bid),
                    _meets_condition(profile.inc_bid, bidder.inc_bid),
                    _meets_condition(profile.dec_bid, bidder.dec_bid),
                    _meets_condition(profile.pass_after, bidder.pass_after)
                ]):
                    result[profile.name] += 1
        return result
