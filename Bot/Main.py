import telebot
from telebot import types
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup
import schedule

bot = telebot.TeleBot('6236696473:AAH_OGgS5jBhtDC7ZRA8lJwXHHZkQCfxZwg')

id_user = []
chat_grup = '-742710832'


def lot(category, message_id, val):
    if val == 'dish':
        ocenka = show_marks()
        for dish in menu_[category]:
            text = ''
            photo1 = ''
            for info in dish:
                if info == dish[1]:
                    text += 'Рейтинг - ' + ocenka[f'{dish[1]}'] + ' ⭐️ \n'
                    text += f'Название - {info}\n'
                elif info == dish[3]:
                    text += f'Стоимость - {info}\n'
                elif info == dish[5]:
                    text += f'Время готовки - {info}\n'
                elif info == dish[2]:
                    photo1 = open(f'img/{info}', 'rb')
                elif info == dish[4]:
                    text += f'Состав - {info}\n'

            keyb_ = types.InlineKeyboardMarkup()
            keyb_.add(types.InlineKeyboardButton('Заказать', callback_data=f'*{dish[1]}'))
            # bot.send_message(message_id, '👇', reply_markup=keyb_)
            bot.send_photo(message_id, photo=photo1, caption=text, reply_markup=keyb_)


def send_lot_in_group():
    pass


def post_lots():
    bot.send_message(chat_grup, 'карточка')




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
        print(message.chat_id)


@bot.callback_query_handler(func=lambda call: True)
def query_handler(call):
    if call.data == 'menu':
        bot.clear_step_handler_by_chat_id(call.message.chat.id)
        bot.send_message(call.from_user.id, 'Выберите категорию')


print("Ready")
bot.infinity_polling()
