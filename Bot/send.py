from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

from Bot.Main import keub_start
from Bot.Bot_ import bot


def send_(chat_id, data):
    bot.send_message(chat_id, data, reply_markup=keub_start())


def send_new_auction(chat_id, data):
    keyb_ = InlineKeyboardMarkup().add(InlineKeyboardButton("Обработать", callback_data='cash_add'))
    bot.send_message(chat_id, data, reply_markup=keyb_)
