import requests
import config


def login():
    values = {'Login': config.username, 'Password': config.password}
    s = requests.Session()
    s.post(config.login_page, data=values)
    return s


def team_check(s):
    r = s.get(config.team_details)
    return r.text


def end_work(s):
    s.close()

def current_level(s, url):
    r = s.get(url)
    return r.text
