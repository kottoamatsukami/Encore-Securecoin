import time

import ccxt as ccxt
import threading

class CEXParser(object):
    def __init__(self, exchanges: list[str]):
        self.exchanges = []
        self.blacklist = dict()

        self.change_exchanges(exchanges)
        self.__cache = {}

    def change_exchanges(self, exchanges: list[str]) -> bool:
        self.exchanges = []
        for exchange in exchanges:
            if AVAILABLE_CEX_EXCHANGES.__contains__(exchange.lower()):
                self.exchanges.append(
                    AVAILABLE_CEX_EXCHANGES[exchange.lower()](
                        {
                            "options": {
                                'defaultType': 'spot'
                            },
                        }
                    )
                )
                self.blacklist[self.exchanges[-1].name] = set()
        assert len(self.blacklist) > 0
        return True

    def parse(self, tickets: list[str]) -> dict:
        # scheme: one exchange -> one thread
        threads = []
        for exchange in self.exchanges:
            thread = threading.Thread(
                target=self.__parse_daemon,
                args=(exchange, tickets)
            )
            threads.append(thread)
            thread.start()

        # Wait for all threads have finished
        for thread in threads:
            thread.join()

        return self.__cache

    def __parse_daemon(self, exchange: ccxt.Exchange, tickets) -> None:
        tickets = set(tickets) - self.blacklist[exchange.name]
        result = []
        for ticket in tickets:
            try:
                data = exchange.fetch_order_book(ticket, limit=1)
                result.append({
                    'ticket': data['symbol'],
                    'bid':    data['bids'][0][0],
                    'ask':    data['asks'][0][0],
                })
            except:
                self.blacklist[exchange.name].add(ticket)
        self.__cache[exchange.name] = result

AVAILABLE_CEX_EXCHANGES = {
    'binance' : ccxt.binance,
    'bybit':    ccxt.bybit,
    'gateio':   ccxt.gateio,
    'huobi':    ccxt.huobi,
}