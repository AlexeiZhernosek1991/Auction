import telebot
from telebot import types
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup
import schedule
import time
import datetime
import threading

from Bot.sql_req import get_lots, is_publish, get_lot

bot = telebot.TeleBot('6236696473:AAH_OGgS5jBhtDC7ZRA8lJwXHHZkQCfxZwg')

id_user = []
chat_grups = -742710832

"""Проверка базы данных на изменение"""


def keyb_lot(id_lot, time_finish):
    keyb = InlineKeyboardMarkup()
    keyb.add(*(types.InlineKeyboardButton('Участвовать', callback_data=f'#{id_lot}'),
               types.InlineKeyboardButton('⏰', callback_data=f'*{time_finish}'),
               types.InlineKeyboardButton('😱', callback_data='info')
               ))
    return keyb


def keyb_lot2(id_lot, time_finish):
    keyb = InlineKeyboardMarkup()
    but1 = InlineKeyboardButton('+10 руб.', callback_data=f'$.10.{id_lot}')
    but2 = InlineKeyboardButton('+20 руб.', callback_data=f'$.20.{id_lot}')
    but3 = InlineKeyboardButton('+30 руб.', callback_data=f'$.30.{id_lot}')
    keyb.row(but1, but2, but3)
    but4 = InlineKeyboardButton('+40 руб.', callback_data=f'$.40.{id_lot}')
    but5 = InlineKeyboardButton('+50 руб.', callback_data=f'$.50.{id_lot}')
    but6 = InlineKeyboardButton('+100 руб.', callback_data=f'$.100.{id_lot}')
    keyb.row(but4, but5, but6)
    but_start = InlineKeyboardButton('Старт', callback_data=f'st.10.{id_lot}')
    keyb.row(but_start)
    but_auto = InlineKeyboardButton('Авто-ставка', callback_data=f'ast.10.{id_lot}')
    keyb.row(but_auto)
    keyb.row(*(types.InlineKeyboardButton('⏰', callback_data=f'*{time_finish}'),
               types.InlineKeyboardButton('😱', callback_data='info')
               ))
    return keyb


def post_lots():
    chat_grup = -742710832
    lots = get_lots()
    if len(lots) < 1:
        pass
    else:
        for lot in lots:
            is_publish(lot['id'])
            keyb = keyb_lot(lot['id'], lot['time_finish'])
            bot.send_media_group(chat_grup,
                                 [telebot.types.InputMediaPhoto(
                                     open(f'D:\Пайтон\Auction\my_auction\media\{photo}', 'rb'))
                                     for photo in lot['photo']])
            bot.send_message(chat_grup, f'Название - {lot["name"]} \n'
                                        f'стоимость - {lot["price"]} белоруских рублей', reply_markup=keyb)


def send_lot_in_group():
    schedule.every(5).seconds.do(post_lots)
    while True:
        schedule.run_pending()
        time.sleep(1)


"""___________________________________"""


@bot.message_handler(
    content_types=['sticker', 'voice', 'audio', 'document', 'photo', 'video', 'caption', 'contact', 'location',
                   'venue'])
def spam(message):
    bot.send_message(message.chat.id, f'не ломай бота пж')
    bot.delete_message(message.chat.id, message.message_id)


@bot.message_handler(content_types=['text'])
def start(message):
    if message.text == '/start':
        bot.send_message(message.chat.id, 'Здравствуйте! \n Вам надо зарегистрироваться')
        bot.send_message(message.chat.id, 'описание')
    if message.text == '/run':
        if message.chat.id == chat_grups:
            bot.send_message(message.chat.id, 'Работает')


@bot.callback_query_handler(func=lambda call: True)
def query_handler(call):
    if call.data[0] == '#':
        print(call.data[1:])
        lot = get_lot(call.data[1:])
        keyb = keyb_lot2(lot['id'], lot['time_finish'])
        bot.send_media_group(call.from_user.id,
                             [telebot.types.InputMediaPhoto(
                                 open(f'D:\Пайтон\Auction\my_auction\media\{photo}', 'rb'))
                                 for photo in lot['photo']])
        bot.send_message(call.from_user.id, f'Название - {lot["name"]} \n'
                                            f'стоимость - {lot["price"]} белоруских рублей', reply_markup=keyb)
    elif call.data[0] == '*':
        time_now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        time_now = datetime.datetime.strptime(time_now, '%Y-%m-%d %H:%M:%S')
        time_finish = datetime.datetime.strptime(call.data[1:], '%Y-%m-%d %H:%M:%S')
        if time_finish > time_now:
            time_ = str(time_finish - time_now)
            bot.answer_callback_query(call.id, f"Осталось {time_} до завершения аукциона", show_alert=True)
        else:
            bot.answer_callback_query(call.id, f"Аукцион завершился", show_alert=True)
    elif call.data == 'info':
        bot.answer_callback_query(call.id, f"Справочная информация", show_alert=True)
    elif call.data[0] == '$':
        list_data = call.data.split('.')
        print(list_data)


# def start_bot():
#     print("Ready")
#     bot.infinity_polling()
#
#
# t1 = threading.Thread(target=start_bot)
# t2 = threading.Thread(target=send_lot_in_group)
#
# t1.start()
# t2.start()

# print("Ready")
# bot.infinity_polling()
