import telebot
from telebot import types
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton
import schedule
import time
import datetime
import threading

from Bot.sql_req import  get_lot, get_user_byers, reg_user_byers, reg_seller_tg, get_seller_tg, \
    tg_id_in_bdinfouser

bot = telebot.TeleBot('6236696473:AAH_OGgS5jBhtDC7ZRA8lJwXHHZkQCfxZwg')

id_user = []
chat_grups = -742710832

"""Клавиатуры"""


def keub_start():
    keyb = ReplyKeyboardMarkup(resize_keyboard=True).add(KeyboardButton('Справочная Информация'))
    return keyb


def keub_reg():
    keyb = InlineKeyboardMarkup().add(
        *(InlineKeyboardButton('Регистрация', url='http://127.0.0.1:8000/register'),
          InlineKeyboardButton('Отмена', callback_data=f'Отмена')))
    return keyb


def keyb_lot(id_lot, time_finish):
    keyb = InlineKeyboardMarkup()
    keyb.add(*(InlineKeyboardButton('Участвовать', callback_data=f'#{id_lot}'),
               InlineKeyboardButton('⏰', callback_data=f'*{time_finish}'),
               InlineKeyboardButton('😱', callback_data='info')
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
    keyb.row(*(InlineKeyboardButton('⏰', callback_data=f'*{time_finish}'),
               InlineKeyboardButton('😱', callback_data='info'),
               InlineKeyboardButton('🧳 информация по лоту', callback_data=f'dop{id_lot}')
               ))
    return keyb

def keyb_start2(id_user):
    if tg_id_in_bdinfouser(id_user):
        keyb_start = InlineKeyboardMarkup().row(InlineKeyboardButton('Пополнить баланс', callback_data=''))




"""Проверка базы данных на изменение"""


def post_lots():
    pass
    # chat_grup = -742710832
    # lots = get_lots()
    # if len(lots) < 1:
    #     pass
    # else:
    #     pass
    # for lot in lots:
    #     is_publish(lot['id'])
    #     keyb = keyb_lot(lot['id'], lot['time_finish'])
    #     bot.send_media_group(chat_grup,
    #                          [telebot.types.InputMediaPhoto(
    #                              open(f'D:\Пайтон\Auction\my_auction\media\{photo}', 'rb'))
    #                              for photo in lot['photo']])
    #     bot.send_message(chat_grup, f'Название - {lot["name"]} \n'
    #                                 f'стоимость - {lot["price"]} белоруских рублей', reply_markup=keyb)


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
    print(message)
    if message.text == '/start' and message.chat.id != chat_grups:
        bot.send_message(message.chat.id, 'Приветствую', reply_markup=keub_start())
        # bot.delete_message(message.chat.id, message.message_id)
    elif message.text == 'Справочная Информация':
        bot.send_message(message.chat.id, 'Информация о правилах пользования ботом')
        bot.delete_message(message.chat.id, message.message_id)
    elif message.text == '/reg' and message.chat.id != chat_grups:
        bot.send_message(message.chat.id, 'Регистрация', reply_markup=keub_reg())
        bot.delete_message(message.chat.id, message.message_id)
        if get_seller_tg(message.from_user.id):
            pass
        else:
            reg_seller_tg(message.from_user.id, message.from_user.username)



@bot.callback_query_handler(func=lambda call: True)
def query_handler(call):
    if call.data[0] == '#':
        if get_user_byers(call.from_user.id):
            pass
        else:
            reg_user_byers(call.from_user.id)
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
        # print(call)
        bot.answer_callback_query(call.id, f"Справочная информация", show_alert=True)
    elif call.data[0] == '$':
        list_data = call.data.split('.')
        print(list_data)
    elif call.data[0:3] == 'dop':
        bot.send_document(call.from_user.id, document=open('D:\Пайтон\Auction\Bot\Inform.rar', 'rb'))
    elif call.data == 'Отмена':
        bot.delete_message(call.from_user.id, call.message.message_id)



def start_bot():
    print("Ready")
    bot.infinity_polling()


t1 = threading.Thread(target=start_bot)
t2 = threading.Thread(target=send_lot_in_group)

t1.start()
t2.start()
