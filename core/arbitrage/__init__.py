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


class Scheme(object):

    def __init__(self, path, actions) -> None:
        self.path = path
        self.actions = actions

    def __repr__(self) -> str:
        log = ''
        i = 0
        for action in self.actions:
            if action.split()[0] in ('SELL', 'BUY'):
                log += f'\t{self.path[i][1]} {self.path[i][0]} {action.split()[0]} : {action.split()[1]}\n'
                i += 1
            else:
                log += f'\t{action}\n'
        return log




def criteria(worst: float, best: float, speed: float):
    assert 0 <= speed <= 1
    return worst*(1-speed) + best*speed