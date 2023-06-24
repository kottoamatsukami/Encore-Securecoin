import ccxt
import time


class ExchangeParser(object):

    def __init__(self, exchanges: list[ccxt.Exchange], tickets: list[str]) -> None:
        self.exchanges = exchanges
        self.tickets = tickets
        self.parse_time = 0
        self.in_cycle = False

    def parse_cycle(self, save_file: str) -> None:

        self.in_cycle = True

        while True:
            start_time = time.time()

            time.sleep(1)

            if not self.in_cycle:
                break

            self.parse_time = time.time() - start_time