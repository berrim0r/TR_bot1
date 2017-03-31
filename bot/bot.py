import telebot

import config

bot = telebot.TeleBot(config.token)

print bot.get_me()


def log(message, answer):
    from datetime import datetime
    print '\n ------'
    print datetime.now()
    print 'Message from {0}. (id = {1})\nText - {2}'.format(message.from_user.first_name,
                                                                   str(message.from_user.id),
                                                                   message.text)
    print answer


@bot.message_handler(commands=['start'])
def handle_start(message):
    user_markup = telebot.types.ReplyKeyboardMarkup(True, True)
    user_markup.row('/start', '/stop')
    user_markup.row('/login', '/team')
    bot.send_message(message.from_user.id, 'Hello!', reply_markup=user_markup)


@bot.message_handler(commands=['stop'])
def handle_stop(message):
    hide_markup = telebot.types.ReplyKeyboardRemove()
    bot.send_message(message.from_user.id, '..', reply_markup=hide_markup)


if __name__ == '__main__':
    bot.polling(none_stop=True)

