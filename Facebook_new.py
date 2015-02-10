__author__ = 'elichai2'

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
import time

driver = webdriver.Firefox()
wait = WebDriverWait(driver, 10)

GROUP_NAME = '**********'
GROUP_ID = '**********'
USER_NAME = '********@*****.***'
PASSWORD = '*********'

def get_settings_list(driver):
    elemList = driver.find_elements_by_xpath("//a[@role = 'button']")
    lst = list()
    for elem in elemList:
        try:
            elem.find_element_by_xpath("./span/i[@class='img sp_0tfZKD-YQv- sx_7db296']")
            lst.append(elem)
        except:
            pass
    return lst


def connect_facebook(user, password, driver):
    elem = driver.find_element_by_id("email")
    elem.send_keys(user)
    elem = driver.find_element_by_id("pass")
    elem.send_keys(password)
    elem.submit()
    return driver


def get_non_admins_dict(driver):
    nonAdmins = dict()
    users = get_settings_list(driver)
    for user in users:
        flag = True
        user.click()
        time.sleep(1)
        elemList = driver.find_elements_by_xpath("//a[@role='menuitem']")
        for elemIn in elemList:
            try:
                 elemIn.find_element_by_xpath("./span[contains(. ,'Make Admin')]")  # Check if 'Make Admin' option exist in the menu
                 for key in nonAdmins:
                     id = user.get_attribute('id')
                     if id == key:
                         flag = False
                         break
                 if flag:
                    print user.get_attribute('id')
                    nonAdmins[user.get_attribute('id')] = elemIn.get_attribute('href')
                 else: break
            except:
                pass
        user.click()
        if not flag:
            break
    return nonAdmins


def make_admin(menu_href, button_href):
    wait.until(EC.element_to_be_clickable((By.ID, menu_href)))
    menu = driver.find_element_by_id(menu_href)
    menu.click()
    time.sleep(1)
    button = driver.find_element_by_xpath("//a[@href='%s']" % button_href)
    button.click()  # Click on 'Make Admin'
    time.sleep(1)
    driver.find_element_by_name("make_admin").click()  # Accept the new Admin
    print "added"

driver.get("https://www.facebook.com/groups/%s/members/" % GROUP_ID)
driver = connect_facebook(USER_NAME, PASSWORD, driver)
assert GROUP_NAME in driver.title
time.sleep(1)

nonAdmins = get_non_admins_dict(driver)
for menu_id, button_href in nonAdmins.iteritems():
    print menu_id
    button_href = button_href.split('https://www.facebook.com')[1]
    print button_href
    make_admin(menu_id, button_href)
    time.sleep(2)
print "FINISHED"

time.sleep(10)
driver.close()

