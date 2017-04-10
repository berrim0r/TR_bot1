# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
import re
import config


def main_text(text):
    soup = BeautifulSoup(text, "lxml")
    zadanie = soup.find(text=u'Task')
    try:
        m = zadanie.find_next()
    except:
        m = 'Oops!'
    return m


def get_time(text):
    soup = BeautifulSoup(text, "lxml")
    try:
        m = soup.find('h3', {'class': 'timer'}).span.text
    except:
        m = 'Oops!'
    return m


def get_vs(text):
    soup = BeautifulSoup(text, 'lxml')
    codes = soup.find('div', {'class': 'cols w100per'})
    m = ''
    try:
        for item in codes.find_all('p'):
            m += item.text + '\n'
    except:
        m = 'Oops!'
    return m


def get_ps(text):
    soup = BeautifulSoup(text, 'lxml')
    codes = soup.find('div', {'class': 'cols w100per'})
    m = ''
    try:
        for item in codes.find_all('p'):
            if "not" not in item.text.split():
                m += item.text + '\n'
    except:
        m = 'Oops!'
    return m


def get_ks(text):
    soup = BeautifulSoup(text, 'lxml')
    codes = soup.find('div', {'class': 'cols w100per'})
    m = ''
    try:
        for item in codes.find_all('p'):
            if "not" in item.text.split():
                m += item.text + '\n'
    except:
        m = 'Oops!'
    return m


def get_vb(text):
    soup = BeautifulSoup(text, 'lxml')
    bonuses = soup.find_all('h3', {'class': re.compile('color_correct|color_bonus')})
    m = ''
    try:
        for item in bonuses:
            m += item.text + '\n'
    except:
        m = 'Oops!'
    return m


def get_kb(text):
    soup = BeautifulSoup(text, 'lxml')
    bonuses = soup.find_all('h3', {'class': 'color_bonus'})
    m = ''
    try:
        for item in bonuses:
            m += item.text + '\n'
    except:
        m = 'Oops!'
    return m


def get_pb(text):
    soup = BeautifulSoup(text, 'lxml')
    bonuses = soup.find_all('h3', {'class': 'color_correct'})
    m = ''
    try:
        for item in bonuses:
            m += item.text + '\n'
            m += item.nextSibling.nextSibling.text
    except:
        m = 'Oops!'
    return m


def get_ha(text):
    soup = BeautifulSoup(text, 'lxml')
    prompts = soup.find_all(text=re.compile(r'Prompt \d'))
    m = ''
    try:
        for item in prompts:
            m += item + ' ' + item.find_next().text + '\n'
    except:
        m = 'Oops!'
    return m


def get_h_num(text, num):
    soup = BeautifulSoup(text, 'lxml')
    prompts = soup.find(text='Prompt %d' % num)
    m = ''
    try:
        m += prompts + ' ' + prompts.find_next().text
    except:
        m = 'Oops!'
    return m


def get_coords(text):
    try:
        m = re.findall(r'(-?\d+\.\d+)', text)
    except:
        m = 'Oops!'
    return m


def code_push(s, text, code, game_num):
    level_id = level_info(text)[0]
    level_number = level_info(text)[1]
    code_data = {'LevelId': level_id, 'LevelNumber': level_number,
                 'LevelAction.Answer': code}
    try:
        s.post(config.game_engine + game_num + '/', code_data)
    except:
        return False
    if is_in(code, get_ps(s.get(config.game_engine + game_num + '/').text).split()):
        return True
    else:
        return False


def bonus_push(s, text, bonus, game_num):
    level_id = level_info(text)[0]
    level_number = level_info(text)[1]
    bonus_data = {'LevelId': level_id, 'LevelNumber': level_number,
                 'BonusAction.Answer': bonus}
    try:
        s.post(config.game_engine + game_num + '/', bonus_data)
    except:
        return False
    if is_in(bonus, get_pb(s.get(config.game_engine + game_num + '/').text).split()):
        return True
    else:
        return False


def is_in(code, ls):
    try:
        if code in map(lambda x: x.encode('utf-8'), ls):
            return True
        else:
            return False
    except:
        return False


def level_info(text):
    soup = BeautifulSoup(text, 'lxml')
    try:
        level_id = soup.find('input', {'name': 'LevelId'}).attrs['value']
        level_number = soup.find('input', {'name': 'LevelNumber'}).attrs['value']
    except:
        level_id, level_number = 0, 0
    return level_id, level_number


def is_logged(s):
    if s is None:
        return False
    else:
        return True
