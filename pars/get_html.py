# -*- coding: utf-8 -*-
import time
from selenium.webdriver.phantomjs.webdriver import WebDriver
import config


def init_driver():
    driver = WebDriver(executable_path=config.phantom_path)
    return driver


def inputs(inp, driver, login_id):
    driver.find_element_by_id(login_id).click()
    driver.find_element_by_id(login_id).clear()
    driver.find_element_by_id(login_id).send_keys(inp)


def login(driver):
    driver.get(config.home_page)
    driver.find_element_by_id("ctl14_ctl04_ctl00_lnkLogin").click()
    inputs(config.username, driver, "txtLogin")
    inputs(config.password, driver, "txtPassword")
    driver.find_element_by_name("EnButton1").click()


def team_info(driver):
    driver.find_element_by_link_text("Моя команда").click()
    page_body = driver.page_source
    with open('text.html', 'w') as output_file:
        output_file.write(page_body.encode('utf-8'))
    time.sleep(10)


def close(driver):
    driver.quit()


driver = init_driver()
login(driver)
team_info(driver)
close(driver)