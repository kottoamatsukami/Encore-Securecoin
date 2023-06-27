from core.telegram_bot import text, keyboards
from aiogram import types, F, Router
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
import aiogram
import random

router = aiogram.Router()

@router.message(Command("start"))
async def start_handler(msg: Message):
    if router.user_cache.__contains__(msg.from_user.id):
        router.user_cache[msg.from_user.id]['username'] = msg.from_user.username
    else:
        router.user_cache[msg.from_user.id] = {'username': msg.from_user.username}

    await msg.answer(random.choice(text.greeting['GB']).format(msg.from_user.first_name))

    if not is_user_whitelisted(msg):
        # New user
        data = (
                int(msg.from_user.id),
                msg.from_user.first_name,
                'GB',
                100,
                'Tinkoff, Sberbank',
                'Tinkoff, Sberbank',
                'Binance, Bybit',
                'Binance, Bybit',
                'USDT',
                3,
                0,
                0.00075,
                1,
                0,
                0,
                '',
                'NGN',
            )
        router.database.insert_data(
            data=data
        )
    await msg.answer(text.menu, reply_markup=keyboards.menu)



@router.message(F.text == "menu")
async def menu(msg: Message):
    if is_user_whitelisted(msg):
        await msg.answer(text.menu, reply_markup=keyboards.menu)
    else:
        await msg.answer("Please type /start for authorization")

######################
# Survey
######################
def survey(msg: Message):
    ...
######################
# CALLBACKS
######################
@router.callback_query(F.data.split(':')[0] == "change_language")
async def change_language(callback: CallbackQuery):
    router.user_cache[callback.from_user.id]['language'] = F.data.split(':')[1]
    await callback.message.answer("The language was successfully changed")

@router.callback_query(F.data == "spot_arbitrage")
async def spot_arbitrage(callback: CallbackQuery):
    info = is_user_whitelisted(callback)
    localisation = info[3]
    if info:
        router.queue.put(
            {
                'user': callback.from_user,
                'callback': callback,
                'task': 'arbitrage',
                'params': info,
            }
        )
        await callback.message.answer(
            text.arbitrage_info[localisation].format(info[4], *info[7:])
        )

    else:
        await callback.message.answer("Please type /start for authorization")

@router.callback_query(F.data == "get_insides")
async def get_inside(callback: CallbackQuery):
    if is_user_whitelisted(callback):
        await callback.message.answer("GET INSIDES")
    else:
        await callback.message.answer("Please type /start for authorization")

@router.callback_query(F.data == "p2p_arbitrage")
async def p2p_arbitrage(callback: CallbackQuery):
    if is_user_whitelisted(callback):
        await callback.message.answer("P2P ARBITRAGE")
    else:
        await callback.message.answer("Please type /start for authorization")

@router.callback_query(F.data == "multi_arbitrage")
async def multi_arbitrage(callback: CallbackQuery):
    if is_user_whitelisted(callback):
        await callback.message.reply("MULTI ARBITRAGE")
    else:
        await callback.message.answer("Please type /start for authorization")

@router.callback_query(F.data == "settings")
async def spot_arbitrage(callback: CallbackQuery):
    if is_user_whitelisted(callback):
        await callback.message.answer("SETTINGS")
    else:
        await callback.message.answer("Please type /start for authorization")

#########################
# OTHER
#########################
def is_user_whitelisted(msg):
    info = router.database.cursor.execute('SELECT * FROM user_data WHERE user_id=?', (msg.from_user.id,))
    if info.fetchone() is None:
        return False
    else:
        return info.fetchone()