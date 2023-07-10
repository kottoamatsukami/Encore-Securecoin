from core.exchanges.DEX import oneinch


VALID_EXCHANGES = {
    '1inch': oneinch.OneInch,
}


class DEXAgregator(object):
    def __init__(self, exchanges: list[str]) -> None:
        self.exchanges = {exchange: VALID_EXCHANGES[exchange.lower()]()
                          for exchange in exchanges
                          if VALID_EXCHANGES.__contains__(exchange.lower())
                          }

    def get_pair_swap(self, pair: str) -> dict:
        result = {}
        for exchange in self.exchanges:
            result[exchange] = self.exchanges[exchange].get_pair_swap(pair)
        return result
