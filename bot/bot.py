# -*- coding: utf-8 -*-
import telebot
import config
from pars import get_html_by_requests, pars
from pars import config as cfg
from pars.pars import is_logged
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
/L - геометка
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
s = None
bot = telebot.TeleBot(config.token)
level_id = 0

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


@bot.message_handler(regexp=r'/login\d')
def handle_login(message):
    global game_num
    game_num = message.text[6:]
    global s
    s = get_html_by_requests.login()
    global level_id
    level_id = pars.level_info(get_html_by_requests.current_level(s, cfg.game_engine + game_num + '/'))[0]
    bot.send_message(message.from_user.id, "I'm in!")

'''реакция бота на команду /q: выход из игрового движка, разлогинивание'''


@bot.message_handler(commands=['q'])
def handle_quit(message):
    get_html_by_requests.end_work(s)
    bot.send_message(message.from_user.id, "I'm done!")

'''Список оставшихся кодов в секторах'''


@bot.message_handler(commands=['ks'])
def handle_ks(message):
    if is_logged(s):
        msg = get_html_by_requests.current_level(s, cfg.game_engine + game_num + '/')
        t = pars.get_ks(msg)
        bot.send_message(message.from_user.id, t)
    else:
        bot.send_message(message.from_user.id, "Хочу залогиниться!") #/ks - оставшиеся коды в секторах

'''Список принятых основных кодов'''


@bot.message_handler(commands=['ps'])
def handle_ps(message):
    if is_logged(s):
        msg = get_html_by_requests.current_level(s, cfg.game_engine + game_num + '/')
        t = pars.get_ps(msg)
        bot.send_message(message.from_user.id, t)
    else:
        bot.send_message(message.from_user.id, "Хочу залогиниться!") #/ps - принятые коды в секторах

'''Полный список основных кодов с указанием принятых'''


@bot.message_handler(commands=['vs'])
def handle_vs(message):
    if is_logged(s):
        msg = get_html_by_requests.current_level(s, cfg.game_engine + game_num + '/')
        t = pars.get_vs(msg)
        bot.send_message(message.from_user.id, t)
    else:
        bot.send_message(message.from_user.id, "Хочу залогиниться!") #/vs - полный список основных кодов с указанием принятых

'''Оставшиеся коды в бонусах'''


@bot.message_handler(commands=['kb'])
def handle_kb(message):
    if is_logged(s):
        msg = get_html_by_requests.current_level(s, cfg.game_engine + game_num + '/')
        t = pars.get_kb(msg)
        bot.send_message(message.from_user.id, t)
    else:
        bot.send_message(message.from_user.id, "Хочу залогиниться!") #/kb - оставшиеся коды в бонусах

'''Принятые бонусы, с указанием текста в них'''


@bot.message_handler(commands=['pb'])
def handle_vb(message):
    if is_logged(s):
        msg = get_html_by_requests.current_level(s, cfg.game_engine + game_num + '/')
        t = pars.get_pb(msg)
        bot.send_message(message.from_user.id, t)
    else:
        bot.send_message(message.from_user.id, "Хочу залогиниться!") #/pb - принятые коды в бонусах

'''Полный список бонусов, с указанием принятых (и текстом в них, если есть)'''


@bot.message_handler(commands=['vb'])
def handle_vb(message):
    if is_logged(s):
        msg = get_html_by_requests.current_level(s, cfg.game_engine + game_num + '/')
        t = pars.get_vb(msg)
        bot.send_message(message.from_user.id, t)
    else:
        bot.send_message(message.from_user.id, "Хочу залогиниться!") #/vb - полный список бонусных кодов с указанием принятых

'''Отправить код в основное поле. Добавить проверку на доступность поля, если поле недоступно - написать пользователю'''


@bot.message_handler(regexp=r'/-.')
def handle_scode(message):
    if is_logged(s):
        code = message.text[2:].encode('utf-8')
        msg = get_html_by_requests.current_level(s, cfg.game_engine + game_num + '/')
        if pars.is_in(code, pars.get_ps(msg).split()):
            bot.reply_to(message, u'Уже был!')
        elif pars.code_push(s, msg, code, game_num):
            bot.reply_to(message, u'Принят!')
        else:
            bot.reply_to(message, u'Не принят!')
    else:
        bot.send_message(message.from_user.id, "Хочу залогиниться!") #/- - отправить код

'''Отправить код в поле для ввода бонусов'''


@bot.message_handler(regexp=r'/b.')
def handle_bcode(message):
    if is_logged(s):
        bonus = message.text[2:].encode('utf-8')
        msg = get_html_by_requests.current_level(s, cfg.game_engine + game_num + '/')
        if pars.bonus_push(s, msg, bonus, game_num):
            bot.reply_to(message, u'Принят!')
        else:
            bot.reply_to(message, u'Не принят!')
    else:
        bot.send_message(message.from_user.id, "Хочу залогиниться!") #/b - отправить бонус

'''Оставшееся время до конца уровня'''


@bot.message_handler(commands=['t'])
def handle_time(message):
    if is_logged(s):
        msg = get_html_by_requests.current_level(s, cfg.game_engine + game_num + '/')
        t = pars.get_time(msg)
        bot.send_message(message.from_user.id, t)
    else:
        bot.send_message(message.from_user.id, "Хочу залогиниться!") #/t - тайминг

'''Отправляет координаты в виде геометки'''


@bot.message_handler(regexp=r'/L \d')
def handle_geotag(message):
    lat = pars.get_coords(message.text[3:])[0]
    lon = pars.get_coords(message.text[3:])[1]
    bot.send_location(message.from_user.id, lat, lon) #/L - геометка
"""
'''Присылает картинку дохода'''


@bot.message_handler(commands=['д'])
def handle_bcode(message):
    if is_logged(s):
        bot.send_photo(message.from_user.id, photo) 
    else:
        bot.send_message(message.from_user.id, "Хочу залогиниться!") #/д - картинка дохода

'''Текст бонуса под номером *'''


@bot.message_handler(regexp=r'bt\d')
def handle_btext(message):
    if is_logged(s):
        bot.send_message(message.from_user.id, 'text bonusa pod nomerom *')
    else:
        bot.send_message(message.from_user.id, "Хочу залогиниться!") #/bt* - текст бонуса под номером *

'''Текст всех бонусов. Если бонус не вбит, прописывает название бонуса и его номер'''


@bot.message_handler(commands=['bta'])
def handle_btext_all(message):
    if is_logged(s):
        bot.send_message(message.from_user.id, 'text vseh bonusov')
    else:
        bot.send_message(message.from_user.id, "Хочу залогиниться!") #/bta - текст всех бонусов

'''Постит всю информацию автоматически в чат, к которому прикреплён'''


@bot.message_handler(commands=['w'])
def handle_welcome(message):
    if is_logged(s):
        bot.send_message(message.chat.id, 'Hello!') #/w - прикрепление к чату
        global chat_id
        chat_id = message.chat.id
    else:
        bot.send_message(message.from_user.id, "Хочу залогиниться!")
"""
'''Выдаёт текст задания в виде:
Время на выполнение
Текст
Картинка (если есть)
корды отдельным текстом (если есть)
корды в виде геометки'''


@bot.message_handler(commands=['z'])
def handle_ztext(message):
    if is_logged(s):
        msg = get_html_by_requests.current_level(s, cfg.game_engine + game_num + '/')
        msg = pars.main_text(msg)
        bot.send_message(message.from_user.id, msg.text)
        h = msg.find('a').get('href')
        l = pars.get_coords(msg.text)
        if h != None:
            bot.send_photo(message.chat.id, h)
        if l != None:
            bot.send_message(message.chat.id, ' '.join(l))
            bot.send_location(message.chat.id, l[0], l[1])
            handle_geotag(' '.join(l))
    else:
        bot.send_message(message.from_user.id, "Хочу залогиниться!") #/z - задание

'''Выдаёт текст всех подсказок. Если подсказка недоступна, добавляет сообщение вида "До подсказки 2 осталось мм:сс"'''


@bot.message_handler(commands=['ha'])
def handle_hint_all(message):
    if is_logged(s):
        msg = get_html_by_requests.current_level(s, cfg.game_engine + game_num + '/')
        t = pars.get_ha(msg)
        bot.send_message(message.from_user.id, t)
    else:
        bot.send_message(message.from_user.id, "Хочу залогиниться!") #/ha - подсказки

'''Выдаёт текст конкретной подсказки'''


@bot.message_handler(regexp=r'/h\d')
def handle_hint_num(message):
    if is_logged(s):
        num = int(message.text[2:])
        msg = get_html_by_requests.current_level(s, cfg.game_engine + game_num + '/')
        t = pars.get_h_num(msg, num)
        bot.send_message(message.from_user.id, t)
    else:
        bot.send_message(message.from_user.id, "Хочу залогиниться!")#/h* - конкретная подсказка по номером *

'''Выдаёт список доступных команд с описанием'''


@bot.message_handler(commands=['help'])
def handle_help(message):
    bot.send_message(message.from_user.id, 'spisok komand') #/help - список команд

'''Реакция на обычный текст, для отладки'''


@bot.message_handler(content_types=['text'])
def handle_help(message):
    bot.send_message(message.from_user.id, 'wololo')  # /help - список команд


if __name__ == '__main__':
    bot.polling(none_stop=True)

