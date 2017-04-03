import requests
import config


def login():
    values = {'Login': config.username, 'Password': config.password}
    with requests.Session() as s:
        r = s.post(config.login_page, data=values)
        r = s.get(config.team_details)
    print r.text

login()
