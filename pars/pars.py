# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
import re


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
    return zadanie.find_next().text

def get_time(text):
    soup = BeautifulSoup(text, "lxml")
    t = soup.find('h3', {'class': 'timer'}).span.text
    return t