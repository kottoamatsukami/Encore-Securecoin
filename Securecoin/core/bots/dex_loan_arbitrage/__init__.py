from core.exchanges.DEX import DEXAgregator
from core.utils import TimeManager

import numpy as np
import itertools

#################################################
# 1) Find the profit crypto pair on two exchanges
# 2) Calculate a spread
# 3) Take a decision about this bundle
# 4) Tell about it user
# 5) User should use it in FURUCOMBO
#################################################


class LoanArbitrageBot(object):
    def __init__(self, options: dict) -> None:
        self.options = options

    def run(self) -> dict:
        # 0) Create time manager
        time_manager = TimeManager()
        # 1) Generate all pairs of cryptocoin
        time_manager.start('Pair Generation')

        valid_pairs = set()
        for pair in itertools.product(*[self.used_coins]*2):
            normal_bundle = True
            for i in range(1, len(pair)):
                if pair[i-1] == pair[i]:
                    normal_bundle = False
            if normal_bundle:
                valid_pairs.add(pair)

        time_manager.end('Pair Generation')
        # 2) Get prices of pairs
        time_manager.start('Get Prices')

        aggregator = DEXAgregator(
            exchanges=self.used_exchanges,
        )
        data = {
                '/'.join(pair): aggregator.get_pair_swap(pair)
                for pair in valid_pairs
                }
        time_manager.end('Get Prices')
        print(time_manager)
        print(data)
