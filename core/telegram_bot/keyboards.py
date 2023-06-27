from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove
################################
# LANGUAGE CHOOSE
################################
language = [
    [
        InlineKeyboardButton(text="🇷🇺", callback_data="change_language:RU"),
        InlineKeyboardButton(text="🇬🇧", callback_data="change_language:GB"),
    ]
]
language = InlineKeyboardMarkup(inline_keyboard=language)
################################
# Main Menu
################################
menu = [
    [
        InlineKeyboardButton(text="💲 Spot arbitrage",           callback_data="spot_arbitrage"),
        InlineKeyboardButton(text="👑 Get insides (Working)",    callback_data="get_insides"),
    ],
    [
        InlineKeyboardButton(text="💳 P2P arbitrage (Working)",  callback_data="p2p_arbitrage"),
        InlineKeyboardButton(text="🚀 Multi arbitrage (Working)",callback_data="multi_arbitrage")
    ],
    # [
    #     InlineKeyboardButton(text="", callback_data=""),
    #     InlineKeyboardButton(text="", callback_data="")
    # ],
    [
        InlineKeyboardButton(text="⚙️ Settings", callback_data="settings")
    ]
]

menu = InlineKeyboardMarkup(inline_keyboard=menu)
################################
# Settings
################################
settings = [
    [
        InlineKeyboardButton(text="💲 Spot arbitrage",   callback_data="spot_arbitrage_settings"),
        InlineKeyboardButton(text="💳 P2P arbitrage",    callback_data="get_insides_settings"),
    ],
    [
        InlineKeyboardButton(text="🔙 Back", callback_data="back")
    ]
]
################################
# Survey
################################
