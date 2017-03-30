import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium import webdriver


def init_driver():
    driver = webdriver.Firefox()
    wait = WebDriverWait(driver, 5)
    return driver, wait


HOME_PAGE = "http://moscow.en.cx/"
driver, wait = init_driver()
driver.get(HOME_PAGE)

log_id = "ctl14_ctl04_ctl00_lnkLogin"
wait.until(ec.element_to_be_clickable((By.ID, log_id)))

log_in = driver.find_element_by_id(log_id).click()

username = driver.find_element_by_id("txtLogin")
password = driver.find_element_by_id("txtPassword")

username.send_keys("berrim0r_en")
password.send_keys("anu11927")

driver.find_element_by_class_name("glassubmit").click()
driver.find_element_by_xpath('/html/body/table[3]/tbody/tr[1]/td/table/tbody/tr/td[1]/div[1]/div/div/table/tbody/tr[6]/td/a').click()

pageBody = driver.page_source

with open('text.html', 'w') as output_file:
    output_file.write(pageBody.encode('utf-8'))
time.sleep(10)

driver.close()
