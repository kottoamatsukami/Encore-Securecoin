from core.arbitrage.parser import ExchangeParser
import ccxt
import threading
import os


class DataParserDaemon(object):

    def __init__(self) -> None:
        self.parsers = dict()
        self.threads = []

    def create_daemon(self, name: str, save_file: str, exchanges: list[str], tickets: list[str]) -> None:
        exchanges = [
            AVAILABLE_CEX_PARSERS[exchange.lower()]
            for exchange in exchanges
            if exchange.lower() in AVAILABLE_CEX_PARSERS
        ]
        assert len(exchanges) != 0

        self.parsers[name] = ExchangeParser(
                                exchanges=exchanges,
                                tickets=tickets,
                            )

        open(save_file, 'w').close()
        thread = threading.Thread(
            target=self.parsers[name].parse_cycle,
            args=[save_file]
        )
        thread.start()
        return

    def remove_demon(self, name: str) -> None:
        self.parsers.pop(name)

    def get_daemon_parse_time(self, name: str) -> float:
        return self.parsers[name].parse_time

    def stop_daemon(self, name: str) -> None:
        self.parsers[name].in_cycle = False

    def continue_daemon(self, name: str) -> None:
        self.parsers[name].in_cycle = True

    def __repr__(self) -> str:
        log = ''
        for i, name in enumerate(self.parsers):
            log += f'{i+1}) {name} {"working" if self.parsers[name].in_cycle else "stopped"}\n'
        return log


AVAILABLE_CEX_PARSERS = {
    'binance': ccxt.binance,
    'bybit':   ccxt.bybit,
    'gateio':  ccxt.gateio,
    'huobi':   ccxt.huobi,
    # 'okx':     ccxt.okx, # Unavailable in Russia
}
# TODO: Dex exchanges
AVAILABLE_DEX_PARSERS = {

}
