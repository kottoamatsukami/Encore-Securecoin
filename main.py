from core.arbitrage import ArbitrageParser, Ticket, Scheme, criteria
from core.telegram_bot import TelegramBot
import tqdm
import itertools
import ccxt

###
exchanges = [
    'binance',
    # 'huobi',
    # 'bybit'
]

blacklisted_crypto = {'NGN'}

tickets = set(
    list(ccxt.binance().load_markets().keys())
) - blacklisted_crypto


cycle_crypto = 'USDT'
max_length_of_bundle = 3
use_only_max = True
deposit = 100
tax = 0.00075
transfer_gaz = 1
target_spread = 1
speed = 0.5
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
        l, r = t.split('/')

        if l in blacklisted_crypto or r in blacklisted_crypto:
            continue

        available_crypto.add(l)
        available_crypto.add(r)
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
        data = parser.last_data
        reformatted_data = dict()

        print('\nParsing Completed')

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

        print('\nData reformatted')

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
                    actions = []
                    for i, part in enumerate(path):
                        ticket, exchange, ask, bid = part

                        if not((last_exchange == exchange) or (last_exchange is None)):
                            profit *= (1 - transfer_gaz/deposit)
                            actions.append(f'TRANSFER: {last_exchange}->{exchange}')

                        target_base, target_quote = ticket.base, ticket.quote
                        source_base, source_quote = bundle[i].split('/')
                        price = criteria(bid, ask, speed)
                        if target_base != source_base:
                            # /
                            profit /= price
                            actions.append(f'BUY {price:.10f}')
                        else:
                            # *
                            profit *= price
                            actions.append(f'SELL {price:.10f}')
                        # add tax
                        profit *= (1 - tax)
                    max_profit = max(max_profit, profit)
                    if target_spread <= (profit/deposit-1)*100:
                        scheme = Scheme(path, actions)
                        msg = f"""
------------<New Arbitrage Situation>------------:
► Deposit: {deposit:.5f} {cycle_crypto},
◯ Total: {profit:.5f} {cycle_crypto},
► Spread: {(profit/deposit-1)*100:.5f} %,
◯ Profit: {profit-deposit:.5f} {cycle_crypto},
►Scheme:
{scheme}"""
                        # call telegram
                        bot.send_message(message=msg)
                        # Do log
                        print(msg)
            progress_bar.set_description(
                f'Parse time: {parser.parse_time}, Max profit: {max_profit}'
            )



if __name__ == '__main__':
    main()