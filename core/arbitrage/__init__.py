from core.arbitrage.CEX import CEXParser
import time
import threading

class ArbitrageParser(object):
    def __init__(self, exchanges: list[str]) -> None:
        self.cex = CEXParser(exchanges)
        self.dex = None

        self.last_data = None
        self.parse_time = float('inf')

    def parse(self, tickets: list[str]) -> None:
        start_time = time.time()

        result = [
            self.cex.parse(tickets),
            {}
        ]
        self.last_data = result
        self.parse_time = time.time() - start_time

class Ticket(object):
    def __init__(self, ticket: str):
        self.ticket, self.alternative = ticket, ticket.split('/')[1] + '/' + ticket.split('/')[0]
        self.base, self.quote = ticket.split('/')
    def __eq__(self, other):
        if isinstance(other, str):
            return self.ticket == other or self.alternative == other

        if isinstance(other, Ticket):
            return self.ticket == other.ticket or self.alternative == other.ticket

    def __hash__(self):
        return hash(self.ticket)

    def __repr__(self) -> str:
        return f'[{self.ticket}]'