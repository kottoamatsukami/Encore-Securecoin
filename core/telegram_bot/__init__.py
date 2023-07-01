import multiprocessing.queues

from core import encore_api
from core import logging
from telegram.ext import Application, CommandHandler, MessageHandler
from core.telegram_bot import handlers

import configparser
import telegram
import dotenv
import os

dotenv.load_dotenv()

class TelegramBot(encore_api.Module):
    def __init__(self, process_name: str, config: configparser.ConfigParser, logger: logging.Logger) -> None:
        self.config = config
        self.logger = logger
        self.token = os.environ.get('BOT_TOKEN')

        super().__init__(process_name=process_name)

        self.logger(
            f'Module {self.__class__.__name__}:{process_name} has been connected'
        )

    def run(self, queue: multiprocessing.Queue) -> None:
        application = Application.builder().token(self.token).build()

        # on different commands - answer in Telegram
        application.add_handler(CommandHandler("start", handlers.start))
        application.add_handler(CommandHandler("menu", handlers.main_menu))

        # on non command i.e message - echo the message on Telegram
        #application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

        # Run the bot until the user presses Ctrl-C
        application.run_polling()