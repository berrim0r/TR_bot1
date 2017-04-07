# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
import re
import config


def parse_team_datafile_bs(text):
    players = []
    soup = BeautifulSoup(text, "lxml")
    team_data = soup.find_all('div', {'id': 'content'})
    for data in team_data:
        cap_name = data.find('a', {'id': 'lnkCaptainInfo'})
        pla_name = data.find('a', {'id': 'lnkLogin'})
        players.append(cap_name.text)
        #for p in pla_name:
        #    players.append(p)
    return players


def main_text(text):
    soup = BeautifulSoup(text, "lxml")
    zadanie = soup.find(text=u'Task')
    return zadanie.find_next()


def get_time(text):
    soup = BeautifulSoup(text, "lxml")
    t = soup.find('h3', {'class': 'timer'}).span.text
    return t


def get_vs(text):
    soup = BeautifulSoup(text, 'lxml')
    codes = soup.find('div', {'class': 'cols w100per'})
    m = ''
    for item in codes.find_all('p'):
        m += item.text + '\n'
    return m


def get_ps(text):
    soup = BeautifulSoup(text, 'lxml')
    codes = soup.find('div', {'class': 'cols w100per'})
    m = ''
    for item in codes.find_all('p'):
        if "not" not in item.text.split():
            m += item.text + '\n'
    return m


def get_ks(text):
    soup = BeautifulSoup(text, 'lxml')
    codes = soup.find('div', {'class': 'cols w100per'})
    m = ''
    for item in codes.find_all('p'):
        if "not" in item.text.split():
            m += item.text + '\n'
    return m


def get_vb(text):
    soup = BeautifulSoup(text, 'lxml')
    bonuses = soup.find_all('h3', {'class': re.compile('color_correct|color_bonus')})
    m = ''
    for item in bonuses:
        m += item.text + '\n'
    return m


def get_kb(text):
    soup = BeautifulSoup(text, 'lxml')
    bonuses = soup.find_all('h3', {'class': 'color_bonus'})
    m = ''
    for item in bonuses:
        m += item.text + '\n'
    return m


def get_pb(text):
    soup = BeautifulSoup(text, 'lxml')
    bonuses = soup.find_all('h3', {'class': 'color_correct'})
    m = ''
    for item in bonuses:
        m += item.text + '\n'
        m += item.nextSibling.nextSibling.text
    return m


def get_ha(text):
    soup = BeautifulSoup(text, 'lxml')
    prompts = soup.find_all(text=re.compile(r'Prompt \d'))
    m = ''
    for item in prompts:
        m += item + ' ' + item.find_next().text + '\n'
    return m


def get_h_num(text, num):
    soup = BeautifulSoup(text, 'lxml')
    prompts = soup.find(text='Prompt %d' % num)
    m = ''
    m += prompts + ' ' + prompts.find_next().text
    return m


def get_coords(text):
    m = re.findall(r'(-?\d+\.\d+)', text)
    return m


def code_push(s, text, code, game_num):
    level_id = level_info(text)[0]
    level_number = level_info(text)[1]
    code_data = {'LevelId': level_id, 'LevelNumber': level_number,
                 'LevelAction.Answer': code}
    s.post(config.game_engine + game_num + '/', code_data)
    if is_in(code, get_ps(s.get(config.game_engine + game_num + '/').text).split()):
        return True
    else:
        return False


def bonus_push(s, text, bonus, game_num):
    soup = BeautifulSoup(text, 'lxml')
    level_id = soup.find('input', {'name': 'LevelId'}).attrs['value']
    level_number = soup.find('input', {'name': 'LevelNumber'}).attrs['value']
    bonus_data = {'LevelId': level_id, 'LevelNumber': level_number,
                 'BonusAction.Answer': bonus}
    s.post(config.game_engine + game_num + '/', bonus_data)
    if is_in(bonus, get_pb(s.get(config.game_engine + game_num + '/').text).split()):
        return True
    else:
        return False


def is_in(code, ls):
    if code.encode('utf-8') in map(lambda x: x.encode('utf-8'), ls):
        return True
    else:
        return False


def level_info(text):
    soup = BeautifulSoup(text, 'lxml')
    level_id = soup.find('input', {'name': 'LevelId'}).attrs['value']
    level_number = soup.find('input', {'name': 'LevelNumber'}).attrs['value']
    return level_id, level_number