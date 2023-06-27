import asyncio

from core.arbitrage import ArbitrageParser, Ticket, Scheme, criteria
from core.logging import Logger
from core.telegram_bot import database
from dotenv import load_dotenv
import configparser
import aiogram
import os
import queue
import threading
import time
import ccxt
import itertools
from aiogram.fsm.storage.memory import MemoryStorage
from core.telegram_bot import handlers


async def start(config: configparser.ConfigParser, logger: Logger):
    load_dotenv(config['Environment']['env_file'])
    token = os.environ.get('BOT_TOKEN')
    bot = aiogram.Bot(
            token=token,
            parse_mode=aiogram.enums.parse_mode.ParseMode.HTML
    )
    dp = aiogram.Dispatcher(storage=MemoryStorage())
    user_cache = dict()
    q = queue.Queue()

    router = handlers.router
    router.database = database.DataManager(config=config)
    router.user_cache = user_cache
    router.queue = q

    dp.include_router(router=router)

    logger('Database has been connected, bot has been started')

    threading.Thread(
        target=worker,
        args=[router, bot]
    ).start()

    await bot.delete_webhook(
        drop_pending_updates=True
    )
    await dp.start_polling(
        bot,
        allowed_updates=dp.resolve_used_update_types()
    )


def worker(router, bot: aiogram.Bot):
    while True:
        if router.queue.qsize() == 0:
            continue
        else:
            task = router.queue.get()
            if task['task'] == 'arbitrage':
                deposit = task['params'][4]
                start_fiat_banks = task['params'][5].split(',')
                finish_fiat_banks = task['params'][6].split(',')
                start_exchanges = task['params'][7].split(',')
                finish_exchanges = task['params'][8].split(',')
                cycle_of = task['params'][9]
                max_length = task['params'][10]
                use_only_max = task['params'][11]
                tax = task['params'][12]
                gaz = task['params'][13]
                target_spread = task['params'][14]
                speed = task['params'][15]
                special_tickets = task['params'][16].split(',')
                blacklisted_tickets = task['params'][17].split(',')

                special_tickets = [
                    'HOT/USDT',
                    'HOT/ETH',
                    'ETH/USDT',
                ]

                # Parsing
                parser = ArbitrageParser(start_exchanges)
                tickets = special_tickets if len(special_tickets) > 1 else ccxt.binance().load_markets().keys()
                print('STARTING')
                available_crypto = set()
                for t in tickets:
                    l, r = t.split('/')
                    if l in blacklisted_tickets or r in blacklisted_tickets:
                        continue
                    available_crypto.add(l)
                    available_crypto.add(r)
                assert (cycle_of in available_crypto)
                bundles = []
                print('BUNDLES')
                for k in range((max_length-1) if use_only_max else 0, max_length):
                    for b in itertools.combinations_with_replacement(available_crypto, k):
                        temp = [cycle_of] + list(b) + [cycle_of]
                        bundle = []
                        for i in range(1, len(temp)):
                            bundle.append(f'{temp[i-1]}/{temp[i]}')
                        bundles.append(bundle)

                # 1) Parse data
                print('PARSING')
                parser.parse(tickets)
                data = parser.last_data
                reformatted_data = dict()

                print('PARSING COMPLETED')

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

                print('Data reformatted')

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
                                    profit *= (1 - gaz/deposit)
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
                            if target_spread <= (profit/deposit-1)*100 or 1:
                                scheme = Scheme(path, actions)
                                msg = f"""
        ------------<New Arbitrage Situation>------------:
        ► Deposit: {deposit:.5f} {cycle_of},
        ◯ Total: {profit:.5f} {cycle_of},
        ► Spread: {(profit/deposit-1)*100:.5f} %,
        ◯ Profit: {profit-deposit:.5f} {cycle_of},
        ►Scheme:
        {scheme}"""
                                # Do log

                                chat_id = task['callback'].message.chat.id
                                asyncio.run(bot.send_message(
                                    chat_id=chat_id,
                                    text=msg
                                ))

