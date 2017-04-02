# -*- coding: utf-8 -*-
import telebot
import config
from pars import get_html, pars


bot = telebot.TeleBot(config.token)
driver = get_html.init_driver()
'''Логи бота'''
print bot.get_me()


def log(message):
    from datetime import datetime
    print '\n ------'
    print datetime.now()
    print 'Message from {0}. (id = {1})\nText - {2}'.format(message.from_user.first_name,
                                                                   str(message.from_user.id),
                                                                   message.text)

'''реакция бота на команду /start: показывает пользовательскую клавиатуру и отправляет пользователю сообщение хелло'''


@bot.message_handler(commands=['start'])
def handle_start(message):
    user_markup = telebot.types.ReplyKeyboardMarkup(True, True)
    user_markup.row('/start', '/stop')
    user_markup.row('/login', '/team')
    bot.send_message(message.from_user.id, 'Hello!', reply_markup=user_markup)

'''реакция бота на команду /stop: убирает пользовательскую клавиатуру и отправляет пользователю сообщение'''


@bot.message_handler(commands=['stop'])
def handle_stop(message):
    hide_markup = telebot.types.ReplyKeyboardRemove()
    get_html.close(driver)
    bot.send_message(message.from_user.id, '..', reply_markup=hide_markup)

'''Реакция бота на команду /login: логинится в двигло (не в игру!) и отправляет пользователю сообщение'''


@bot.message_handler(commands=['login'])
def handle_login(message):
    get_html.login(driver)
    bot.send_message(message.from_user.id, "I'm in!")


'''Реакция бота на команду /team: логинится в двигло (не в игру!) и отправляет пользователю сообщение'''


@bot.message_handler(commands=['team'])
def handle_team(message):
    get_html.team_info(driver)
    pars.parse_team_datafile_bs('text.html')
    mes = pars.get_team_info()
    for i in mes:
        bot.send_message(message.from_user.id, i)


if __name__ == '__main__':
    bot.polling(none_stop=True)
