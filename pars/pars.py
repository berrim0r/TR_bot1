# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
import re

def read_file(filename):
    with open(filename) as input_file:
        text = input_file.read()
    return text


def parse_team_datafile_bs(filename):
    results = []
    text = read_file(filename)

    soup = BeautifulSoup(text, 'lxml')
    team_data = soup.find_all('div', {'id': 'content'})



    for data in team_data:
        rasd = data.find_all('span', {'class': 'white_bold14'})
        id = data.find_all('td', {'height': '18'})
        cap_name = data.find('a', {'id': 'lnkCaptainInfo'})
        pla_name = data.find('a', {'id': 'lnkLogin'})

        for r in rasd:
            print r.text
        print id

        for i in id:
            span = re.search("(</span>)([0-9]+)", i.replace('\n', ''))
            #if span: num = span.group(2)
            #print num
            print 'id ' + i.text[0:len(i.text) - 4]

        for c in cap_name:
            print c

        for p in pla_name:
            print p

    return results

d = parse_team_datafile_bs('text.html')
print d
for key in d:
    print d[key]
