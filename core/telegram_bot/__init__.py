import requests
import telebot


class TelegramBot(object):
    def __init__(self, bot_token: str, chat_id: str):
        self.bot_token = bot_token
        self.chat_id = chat_id

    def send_message(self, message: str) -> None:
        params = params = {
            'chat_id': self.chat_id,
            'text':    message,
        }
        response = requests.get('https://api.telegram.org/bot' + self.bot_token + '/sendMessage', params=params)