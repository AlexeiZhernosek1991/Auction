from Bot.Main import bot, keub_start


def send_(chat_id, data):
    bot.send_message(chat_id, data, reply_markup=keub_start())