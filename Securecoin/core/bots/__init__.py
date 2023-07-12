from core.bots.dex_loan_arbitrage import LoanArbitrageBot


class BotAgregator(object):
    def __init__(self) -> None:
        self.bot_map = {
            'DEX_arb': LoanArbitrageBot,
        }

    def run(self, type_: str, options: dict) -> dict:
        bot = self.bot_map[type_](options)
        bot.
