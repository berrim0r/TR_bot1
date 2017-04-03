# -*- coding: utf-8 -*-
import telebot
import config
import re
from pars import get_html_by_requests, pars
from pars import config as cfg
'''
КОДЫ
/ks - оставшиеся коды в секторах
/ps - принятые коды в секторах
/vs - полный список основных кодов с указанием принятых
/kb - оставшиеся коды в бонусах
/pb - принятые коды в бонусах
/vb - полный список бонусных кодов с указанием принятых
/- - отправить код
/b - отправить бонус
ИНФОРМАЦИЯ
/t - тайминг
/л - геометка
/д - картинка дохода
/bt* - текст бонуса под номером *
/bta - текст всех бонусов
/w - прикрепление к чату
/q - выйти из движка
/login 123456 - зайти в игру с номером 123456
ЗАДАНИЕ
/z - задание
/ha - подсказки
/h* - конкретная подсказка по номером *
/help - список команд

Примечания к коду. Примечания пишутся с новой строки под кодом в виде
/-123dr
синий, на подоконнике"'''

bot = telebot.TeleBot(config.token)

'''Логи бота'''
print bot.get_me()


def log(message):
    from datetime import datetime
    print '\n ------'
    print datetime.now()
    print 'Message from {0}. (id = {1})\nText - {2}'.format(message.from_user.first_name,
                                                                   str(message.from_user.id),
                                                                   message.text)

'''Реакция бота на команду /login 123456: логинится в двигло и заходит в игру, отправляет пользователю сообщение'''


@bot.message_handler(regexp=r'login \d')
def handle_login(message):
    game_num = message.text.split()[1]
    print game_num
    global s
    s = get_html_by_requests.login()
    if cfg.username in pars.parse_team_datafile_bs(get_html_by_requests.team_check(s)):
        bot.send_message(message.from_user.id, "I'm in!")
    else:
        bot.send_message(message.from_user.id, "I'm not in!")

'''реакция бота на команду /q: выход из игрового движка, разлогинивание'''


@bot.message_handler(commands=['q'])
def handle_quit(message):
    get_html_by_requests.end_work(s)
    bot.send_message(message.from_user.id, "I'm done!")

'''Список оставшихся кодов в секторах'''


@bot.message_handler(commands=['ks'])
def handle_ks(message):
    bot.send_message(message.from_user.id, 'ostalos osnovnih') #/ks - оставшиеся коды в секторах

'''Список принятых основных кодов'''


@bot.message_handler(commands=['ps'])
def handle_ps(message):
    bot.send_message(message.from_user.id, 'prinyato osnovnih') #/ps - принятые коды в секторах

'''Полный список основных кодов с указанием принятых'''


@bot.message_handler(commands=['vs'])
def handle_vs(message):
    bot.send_message(message.from_user.id, 'vsego osnovnih') #/vs - полный список основных кодов с указанием принятых

'''Оставшиеся коды в бонусах'''


@bot.message_handler(commands=['kb'])
def handle_kb(message):
    bot.send_message(message.from_user.id, 'ostalos bonusov') #/kb - оставшиеся коды в бонусах

'''Принятые бонусы, с указаниемтекста в них'''


@bot.message_handler(commands=['pb'])
def handle_vb(message):
    bot.send_message(message.from_user.id, 'prinyato bonusov') #/pb - принятые коды в бонусах

'''Полный список бонусов, с указанием принятых (и текстом в них, если есть)'''


@bot.message_handler(commands=['vb'])
def handle_vb(message):
    bot.send_message(message.from_user.id, 'vsego bonusov') #/vb - полный список бонусных кодов с указанием принятых

'''Отправить код в основное поле. Добавить проверку на доступность поля, если поле недоступно - написать пользователю'''


@bot.message_handler(commands=['-'])
def handle_scode(message):
    bot.send_message(message.from_user.id, 'prinyat osnovnoi')
    bot.send_message(message.from_user.id, 'prinyat bonusnii')
    bot.send_message(message.from_user.id, 'neverniy') #/- - отправить код

'''Отправить код в поле для ввода бонусов'''


@bot.message_handler(commands=['b'])
def handle_bcode(message):
    bot.send_message(message.from_user.id, 'prinyat')
    bot.send_message(message.from_user.id, 'neverniy') #/b - отправить бонус

'''Оставшееся время до конца уровня'''


@bot.message_handler(commands=['t'])
def handle_time(message):
    bot.send_message(message.from_user.id, 'vremya na urovne') #/t - тайминг

'''Отправляет координаты в виде геометки'''


@bot.message_handler(commands=['л'])
def handle_geotag(message):
    bot.send_location(message.from_user.id, latitude, longitude, ) #/л - геометка

'''Присылает картинку дохода'''


@bot.message_handler(commands=['д'])
def handle_bcode(message):
    bot.send_photo(message.from_user.id, photo) #/д - картинка дохода

'''Текст бонуса под номером *'''


@bot.message_handler(commands=['bt'])
def handle_btext(message):
    bot.send_message(message.from_user.id, 'text bonusa pod nomerom *') #/bt* - текст бонуса под номером *

'''Текст всех бонусов. Если бонус не вбит, прописывает название бонуса и его номер'''


@bot.message_handler(commands=['bta'])
def handle_btext_all(message):
    bot.send_message(message.from_user.id, 'text vseh bonusov') #/bta - текст всех бонусов

'''Постит всю информацию автоматически в чат, к которому прикреплён'''


@bot.message_handler(commands=['w'])
def handle_welcome(message):
    bot.send_message(message.chat.id, 'Hello!') #/w - прикрепление к чату
    return message.chat.id

'''Выдаёт текст задания в виде:
Время на выполнение
Текст
Картинка (если есть)
корды отдельным текстом (если есть)
корды в виде геометки'''


@bot.message_handler(commands=['z'])
def handle_ztext(message):
    bot.send_message(message.from_user.id, 'text zadaniya') #/z - задание

'''Выдаёт текст всех подсказок. Если подсказка недоступна, добавляет сообщение вида "До подсказки 2 осталось мм:сс"'''


@bot.message_handler(commands=['ha'])
def handle_hint_all(message):
    bot.send_message(message.from_user.id, 'text vseh podskazok') #/ha - подсказки

'''Выдаёт текст конкретной подсказки'''


@bot.message_handler(commands=['h'])
def handle_hint_num(message):
    bot.send_message(message.from_user.id, 'text podskazki pod nomerom *') #/h* - конкретная подсказка по номером *

'''Выдаёт список доступных команд с описанием'''


@bot.message_handler(commands=['help'])
def handle_help(message):
    bot.send_message(message.from_user.id, 'spisok komand') #/help - список команд


if __name__ == '__main__':
    bot.polling(none_stop=True)
