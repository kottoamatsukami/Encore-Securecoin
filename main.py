from core.arbitrage import ArbitrageParser, Ticket
from core.telegram_bot import TelegramBot
import tqdm
import itertools


###
exchanges = [
    'binance',
    'huobi',
    'bybit'
]

tickets = {
    # Hot triangle
    'HOT/USDT',
    'HOT/ETH',
    'ETH/USDT',
    # IRIS triangle
    'IRIS/USDT',
    'IRIS/BTC',
    'BTC/USDT',
    # DOT
    'DOT/USDT',
    'DOT/BNB',
    'DOT/ETH',
    'DOT/BTC',
    # BNB
    'BNB/USDT',
    'BNB/BUSD'
}

cycle_crypto = 'USDT'
max_length_of_bundle = 3
use_only_max = True
deposit = 100
tax = 0.00075
transfer_gaz = 1
target_spead = 0.5
###

def main():
    parser = ArbitrageParser(exchanges)
    bot = TelegramBot(
        bot_token=input('Telegram Bot token (https://t.me/encore_securebot): '),
        chat_id=input('Chat ID: '),
    )
    bot.send_message('Starting Parsing...')
    progress_bar = tqdm.tqdm(range(5000))

    available_crypto = set()
    for t in tickets:
        available_crypto.add(t.split('/')[0])
        available_crypto.add(t.split('/')[1])
    assert (cycle_crypto in available_crypto)

    bundles = []
    for k in range((max_length_of_bundle-1) if use_only_max else 0, max_length_of_bundle):
        for b in itertools.combinations_with_replacement(available_crypto, k):
            temp = [cycle_crypto] + list(b) + [cycle_crypto]
            bundle = []
            for i in range(1, len(temp)):
                bundle.append(f'{temp[i-1]}/{temp[i]}')
            bundles.append(bundle)


    for _ in progress_bar:
        # 1) Parse data
        parser.parse(tickets)
        progress_bar.set_description(
            f'Parse time: {parser.parse_time}'
        )
        data = parser.last_data
        reformatted_data = dict()

        # 2) Reformatting the data
        for type_ in data:
            for exchange in type_.keys():
                for result in type_[exchange]:
                    if reformatted_data.__contains__(result['ticket']):
                        ticket = Ticket(result['ticket'])
                        reformatted_data[ticket].append(
                            [ticket, exchange, result['bid'], result['ask']]
                        )
                    else:
                        ticket = Ticket(result['ticket'])
                        reformatted_data[Ticket(result['ticket'])] = [
                            [ticket, exchange, result['bid'], result['ask']]
                        ]
        # 3) Analyze bundles
        max_profit = 0
        for bundle in bundles:
            biection = []
            for component in bundle:
                for available_tickets in reformatted_data.keys():
                    if available_tickets == component:
                        biection.append(available_tickets)
                        break
            if len(biection) == len(bundle):
                paths = [reformatted_data[biection[i]] for i in range(len(biection))]
                all_paths = itertools.product(*paths)
                for path in all_paths:
                    profit = deposit
                    last_exchange = None
                    for i, part in enumerate(path):
                        ticket, exchange, ask, bid = part

                        if not((last_exchange == exchange) or (last_exchange is None)):
                            profit *= (1 - transfer_gaz/deposit)

                        target_base, target_quote = ticket.base, ticket.quote
                        source_base, source_quote = bundle[i].split('/')
                        if target_base != source_base:
                            # /
                            profit /= ask
                        else:
                            # *
                            profit *= bid
                        # add tax
                        profit *= (1 - tax)
                    max_profit = max(max_profit, profit)
                    if (profit/deposit-1)*100 >= target_spead:
                        msg = f"""
New Arbitrage Situation:
Scheme: {path},
► Deposit: {deposit:.5f} {cycle_crypto},
◯ Total: {profit:.5f} {cycle_crypto},
► Spread: {(profit/deposit-1)*100:.5f} %,
◯ Profit: {profit-deposit:.5f} {cycle_crypto},
"""
                        # call telegram
                        bot.send_message(message=msg)
                        # Do log
                        print(msg)



if __name__ == '__main__':
    main()