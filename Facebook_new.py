#! /usr/bin/env python
__author__ = 'elichai2'

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common import exceptions
import time
import logging
import sys

driver = webdriver.Firefox()
wait_time = 10
wait = WebDriverWait(driver, wait_time)
logging.getLogger('selenium.webdriver.remote.remote_connection').setLevel(logging.ERROR)
logger = logging.getLogger('Main')
logging.basicConfig(filename='facebook.log', level=logging.DEBUG, format=
                    '%(asctime)s: %(levelname)s: %(name)s: %(message)s', datefmt='%Y-%m-%d,%H:%M:%S')

GROUP_NAME = '********'
GROUP_ID = '*************'
USER_NAME = '*****@*****.***'
PASSWORD = '***********'


def connect_facebook(user, password, driver):
    elem = driver.find_element_by_id("email")
    elem.send_keys(user)
    elem = driver.find_element_by_id("pass")
    elem.send_keys(password)
    elem.submit()
    return driver


def make_admin(driver):
    try:
        # Find all the buttons in the page
        elem_list = driver.find_elements_by_xpath("//a[@role = 'button'][@aria-label = 'Member Settings']")
        logger.info('found buttons')
    except exceptions.NoSuchElementException:
        logger.error("haven't found any member settings button in the page Exception:\n{0}".format(sys.exc_info()))
        # logger.error("haven't found any member settings button in the page")
        raise NameError
    for elem in elem_list:
        try:
            elem.click()  # Click on the button to open the menu
            # Find admin menu and click on it
            elem = driver.find_element_by_xpath("//a[@role='menuitem'][contains(@href, 'add_admin')]")
            elem.click()
            wait.until(EC.element_to_be_clickable((By.NAME, "make_admin")))
            driver.find_element_by_name("make_admin").click()  # Accept the admin
            wait.until(EC.staleness_of(elem))
            logger.debug('Added')
            return make_admin(driver)
        except exceptions.NoSuchElementException:
            pass
        except exceptions.ElementNotVisibleException:
            logger.error("Toggle button isn't clickable. Exception: \n{0}".format(sys.exc_info()))
            # logger.error("Toggle button isn't clickable")
            pass
    return 0

logger.debug('START')
driver.get("https://www.facebook.com/groups/%s/members/?order=date&member_query=" % GROUP_ID)
driver = connect_facebook(USER_NAME, PASSWORD, driver)
while True:
    if driver.current_url != "https://www.facebook.com/groups/%s/members/" % GROUP_ID:
        driver.get("https://www.facebook.com/groups/%s/members/" % GROUP_ID)
    try:
        assert GROUP_NAME in driver.title
    except AssertionError:
        logger.error(GROUP_NAME + ' not in title: ' + driver.title)

    try:
        wait.until(EC.presence_of_element_located((By.ID, 'groupsJumpTitle')))
    except Exception as e:
        logger.error("The group name button doesn't exist, even after {0} seconds. Error: \n{1}".format(wait_time, e))
        time.sleep(5)
        continue
    try:
        make_admin(driver)
        logger.debug("Everyone is Admin")
    except NameError:
        time.sleep(5)
        continue

    time.sleep(20)

print "DONE"
time.sleep(8)
driver.close()