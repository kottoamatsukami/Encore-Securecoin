import telegram
from telegram import ForceReply, Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters
from core.telegram_bot import text


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /start is issued."""
    user = update.effective_user
    await update.message.reply_html(
        text=text.greeting,
        reply_markup=ForceReply(selective=True),
    )

async def main_menu(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a keyboard when the command /menu is issued."""
    user = update.effective_user
    await update.message.reply_text(
        text=text.main_menu_title,
        reply_markup=telegram.InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    telegram.InlineKeyboardButton(text=text.main_menu_spot_arbitrage_btn, callback_data='spot_arbitrage'),
                    telegram.InlineKeyboardButton(text=text.main_menu_p2p_arbitrage_btn, callback_data='p2p_arbitrage'),
                ],
                [
                    telegram.InlineKeyboardButton(text=text.main_menu_multi_arbitrage_btn, callback_data='multi_arbitrage'),
                    telegram.InlineKeyboardButton(text=text.main_menu_whale_trading_btn, callback_data='whale_trading'),
                ],
                [
                    telegram.InlineKeyboardButton(text=text.main_menu_settings, callback_data='settings'),
                ]

            ]
        )
    )


