__author__ = 'elichai2'

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

driver = webdriver.Firefox()
wait = WebDriverWait(driver, 10)

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
    elemList = driver.find_elements_by_xpath("//a[@role = 'button']")  # Find all the buttons in the page
    for elem in elemList:
        try:
            elem.find_element_by_xpath("./span/i[@class='img sp_0tfZKD-YQv- sx_7db296']")  # Check if it's a user toggle button
            print 'found'
            elem.click()  # Click on the button to open the menu
            # wait.until(EC.element_to_be_clickable((By.XPATH, "//a[@role='menuitem']")))
            elemList = driver.find_elements_by_xpath("//a[@role='menuitem']") # Find all Menus
            for elemIn in elemList:
                try:
                    elemIn.find_element_by_xpath("./span[contains(. ,'Make Admin')]")  # Check if 'Make Admin' option exist in the menu
                    elemIn.click()  # Click on it
                    # wait.until(EC.element_to_be_clickable((By.NAME, "make_admin")))
                    driver.find_element_by_name("make_admin").click()  # Accept the admin
                    print 'Added'
                    wait.until(EC.staleness_of(elemIn))
                    return make_admin(driver)
                except:
                    pass
        except:
            pass
    return 0

driver.get("https://www.facebook.com/groups/%s/members/?order=date&member_query=" % GROUP_ID)
driver = connect_facebook(USER_NAME, PASSWORD, driver)
assert GROUP_NAME in driver.title

wait.until(EC.presence_of_element_located((By.ID, 'groupsJumpTitle')))
make_admin(driver)

print "DONE"
time.sleep(8)
driver.close()

