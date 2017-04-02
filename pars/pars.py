# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
import re


def read_file(filename):
    with open(filename) as input_file:
        text = input_file.read()
    return text


def parse_team_datafile_bs(filename):
    results = []
    players = []
    num = []
    text = read_file(filename)
    soup = BeautifulSoup(text, "lxml")
    team_data = soup.find_all('div', {'id': 'content'})
    for data in team_data:
        rasd = data.find_all('span', {'class': 'white_bold14'})
        player_id = data.find_all('td', {'height': '18'})
        cap_name = data.find('a', {'id': 'lnkCaptainInfo'})
        pla_name = data.find('a', {'id': 'lnkLogin'})
        for i in player_id:
            span = re.search("(</span>)([0-9]+)", str(i).replace('\n', ''))
            if span: num.append(span.group(2))
        players.append(cap_name.text)
        for p in pla_name:
            players.append(p)
        for r in range(len(rasd)):
            if r >= len(player_id):
                results.append({rasd[r].text: {'empty': 'empty'}})
            else:
                results.append({rasd[r].text: {'id': 'id ' + num[r], 'name': players[r]}})
    return results

def get_team_info():
    d = parse_team_datafile_bs('text.html')
    mes = []
    for item in d:
        s = ''
        for key in item:
            for key1 in item[key]:
                s += item[key][key1] + ' '
        mes.append(key + ' ' + s[:len(s) - 1])
    return mes