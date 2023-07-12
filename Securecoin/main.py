import time

from core import (
    logging,
    cli,
    utils,
    worker,
)
from dotenv import load_dotenv
import configparser
import os

load_dotenv()


def main(*args):
    # 0) Get the configuration from the config file (./data/config.ini)
    config = configparser.ConfigParser()
    config.read('./data/config.ini')
    # 1) Connect the logger module
    logger = logging.Logger(
        config=config
    )
    # 2) Connect the OS manager
    os_manager = utils.OSManager(
        root_path=os.getcwd(),
        config=config,
        logger=logger,
    )
    # 3) Create worker
    worker_deemon = worker.Worker(
        config=config,
        logger=logger,
    )

    # 4) Create the menu
    menu = cli.ConsoleMenu(config=config, logger=logger)
    # --- 0 level
    MAIN_MENU = cli.Menu(
        name='Main Menu',
        colors=['white', 'black'],
        styles=[],
        additional_text=core.cli_updated.text.menu,
        parent=None,
        multiple_choice=False,
    )
    # --- 1 level
    ARBITRAGE = cli.Menu(
        name='Arbitrage',
        colors=['black', 'green', 'white', 'black', 'black', 'white'],
        styles=[],
        additional_text=core.cli_updated.text.arbitrage_menu,
        parent='Main Menu',
    )
    DEFI = cli.Menu(
        name='Defi',
        colors=['black', 'green', 'white', 'black', 'black', 'white'],
        styles=[],
        additional_text='NOTE IN WORKING',
        parent='Main Menu'
    )
    SCHEDULE = cli.Menu(
        name='Schedule',
        colors=['black', 'green', 'white', 'black', 'black', 'white'],
        styles=[],
        additional_text=core.cli_updated.text.schedule_menu,
        parent='Main Menu',
    )
    EXIT = cli.Menu(
        name='Exit',
        colors=['black', 'green', 'white', 'black', 'black', 'white'],
        styles=[],
        additional_text=None,
        parent='Main Menu',
    )
    # --- 2 level (Arbitrage)
    CEX_AND_DEX = cli.Menu(
        name='CEX And DEX',
        colors=['black', 'green', 'white', 'black', 'black', 'white'],
        styles=[],
        additional_text='NOTE IN PROGRESS',
        parent='Arbitrage',
    )
    CEX = cli.Menu(
        name='CEX',
        colors=['black', 'green', 'white', 'black', 'black', 'white'],
        styles=[],
        additional_text='NOTE IN PROGRESS',
        parent='Arbitrage',
    )
    DEX = cli.Menu(
        name='DEX',
        colors=['black', 'green', 'white', 'black', 'black', 'white'],
        styles=[],
        additional_text=core.cli_updated.text.config_menu,
        parent='Arbitrage',
        multiple_choice=True,
    )
    # --- 2 level (Defi)
    WATCH_WALLETS = cli.Menu(
        name='Watch Wallets',
        colors=['black', 'green', 'white', 'black', 'black', 'white'],
        styles=[],
        additional_text='NOTE IN PROGRESS',
        parent='Defi',
    )
    NEW_COINS = cli.Menu(
        name='New Coins',
        colors=['black', 'green', 'white', 'black', 'black', 'white'],
        styles=[],
        additional_text='NOTE IN PROGRESS',
        parent='Defi',
    )
    WHALE_TRADING = cli.Menu(
        name='Whale Tracking',
        colors=['black', 'green', 'white', 'black', 'black', 'white'],
        styles=[],
        additional_text='NOTE IN PROGRESS',
        parent='Defi',
    )
    # --- 2 level (Schedule Menu)
    LAUNCH_WORK = cli.Menu(
        name='Launch Work',
        colors=['black', 'green', 'white', 'black', 'black', 'white'],
        styles=[],
        additional_text=core.cli_updated.text.schedule_menu,
        parent='Schedule',
    )
    STOP_WORK = cli.Menu(
        name='Stop Work',
        colors=['black', 'green', 'white', 'black', 'black', 'white'],
        styles=[],
        additional_text=core.cli_updated.text.schedule_menu,
        parent='Schedule',
    )
    # --- 3 level (CEX_AND_DEX)
    ...
    # --- 3 level (CEX)
    ...
    # --- 3 level (DEX)
    USE_FLASH_LOAN = cli.Menu(
        name='Use Flash Loan',
        colors=['black', 'green', 'white', 'black', 'black', 'white'],
        styles=[],
        additional_text=core.cli_updated.text.dex_arbitrage_menu,
        parent='DEX',
    )
    USE_TELEGRAM_BOT = cli.Menu(
        name='Use Telegram Bot',
        colors=['black', 'green', 'white', 'black', 'black', 'white'],
        styles=[],
        additional_text=core.cli_updated.text.dex_arbitrage_menu,
        parent='DEX'
    )
    USE_UNISWAP = cli.Menu(
        name='Uniswap',
        colors=['black', 'green', 'white', 'black', 'black', 'white'],
        styles=[],
        additional_text=core.cli_updated.text.dex_arbitrage_menu,
        parent='DEX',
    )
    USE_SUSHISWAP = cli.Menu(
        name='Sushiswap',
        colors=['black', 'green', 'white', 'black', 'black', 'white'],
        styles=[],
        additional_text=core.cli_updated.text.dex_arbitrage_menu,
        parent='DEX',
    )
    USE_1INCH = cli.Menu(
        name='1INCH',
        colors=['black', 'green', 'white', 'black', 'black', 'white'],
        styles=[],
        additional_text=core.cli_updated.text.dex_arbitrage_menu,
        parent='DEX',
    )
    USE_PANCAKESWAP = cli.Menu(
        name='Pancakeswap',
        colors=['black', 'green', 'white', 'black', 'black', 'white'],
        styles=[],
        additional_text=core.cli_updated.text.dex_arbitrage_menu,
        parent='DEX',
    )

    menu.add_menus(
        menus=[
            MAIN_MENU,
            ARBITRAGE, DEFI, SCHEDULE, EXIT,
            CEX_AND_DEX, CEX, DEX, LAUNCH_WORK, STOP_WORK, WATCH_WALLETS, NEW_COINS, WHALE_TRADING,
            USE_FLASH_LOAN, USE_TELEGRAM_BOT, USE_PANCAKESWAP, USE_SUSHISWAP, USE_UNISWAP, USE_1INCH
        ]
    )

    # 4) Start menu
    work_schedule = []
    cli.greeting(config=config)
    while True:
        res = menu.run(MAIN_MENU)
        if len(res) == 0:
            continue
        elif res[0] == 'Exit':
            break
        elif res[0] == 'Launch Work':
            work_table = {}
            for work in work_schedule:
                while True:
                    os.system('cls')
                    print(f'Give name of this task: {work}')
                    name = input('>>>')
                    print(f'Confirm? {name} (y/N): ', end='')
                    if input().lower() in ('y', 'yes'):
                        break
                work_table[name] = work
            os.system('cls')
            print('Starting schedule...')
            for work in work_table:
                worker_deemon.add_work(work_table[work])
            worker_deemon.start_daemon()
            print('Complete, daemon started!')
            while True:
                time.sleep(float(config['Options']['worker_timeout']))
                out = worker_deemon.get_output()
                for echo in out:
                    logger.info(
                        f'[DAEMON]: {echo}'
                    )
        else:
            work_schedule.append(res)

    # Clear logs if it noted in the config file
    if config['Options']['clear_logs'].lower() == 'true':
        os_manager.clear_dir(
            dir_path=config['Logging']['logging_path'],
            deep=True,
        )


if __name__ == '__main__':
    import sys
    main(sys.argv)
