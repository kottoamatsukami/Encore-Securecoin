from core import cli
from core import telegram_bot
from core import logging
from core import encore_api
from core import worker

import configparser


# from core.telegram_bot import start

# import asyncio

def main():
    ####################################
    # Initial
    ####################################
    config = configparser.ConfigParser()
    config.read('./config.ini')
    logger = logging.Logger(config=config)

    ####################################
    # Prepare modules
    ####################################
    cli_module = cli.CLI(
        process_name='CLI',
        config=config,
        logger=logger,
    )
    bot_module = telegram_bot.TelegramBot(
        process_name='TGBot',
        config=config,
        logger=logger,
    )
    worker_module = worker.Worker(
        process_name='Worker',
        config=config,
        logger=logger,
    )
    ####################################
    # Launch application
    ####################################
    app = encore_api.Application(
        cli_module,
        bot_module,
        worker_module,
        config=config,
        logger=logger,
    )
    app.run()



if __name__ == '__main__':
    main()