
from core.logging import Logger
from core.telegram_bot import start
import tqdm
import configparser
import asyncio

def main():
    config = configparser.ConfigParser()
    config.read('./config.ini')

    logger = Logger(config=config)

    asyncio.run(
        start(
            config=config,
            logger=logger,
        )
    )





if __name__ == '__main__':
    main()