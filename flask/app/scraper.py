from copy import deepcopy
import os
import time

from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys

from time import sleep, strftime
from random import randint
import pandas as pd


def set_chrome_options() -> None:
    """Sets chrome options for Selenium.
    Chrome options for headless browser is enabled.
    """
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_prefs = {}
    chrome_options.experimental_options["prefs"] = chrome_prefs
    chrome_prefs["profile.default_content_settings"] = {"images": 2}
    return chrome_options


def login(driver, account_username, account_password):
    driver.get('https://www.instagram.com/accounts/login/?source=auth_switcher')
    sleep(3)
    username = driver.find_element_by_name('username')
    username.send_keys(account_username)
    password = driver.find_element_by_name('password')
    password.send_keys(account_password)
    buttons = driver.find_elements_by_tag_name('button')
    login_button = [button for button in buttons if button.text == 'Log In'][0]
    login_button.click()
    sleep(4)
    buttons = driver.find_elements_by_tag_name('button')
    not_now_button = [button for button in buttons if button.text == 'Not Now'][0]
    not_now_button.click()
    sleep(4)

    return


def navigate_to_account(driver, account_name):

    searchbar = driver.find_element_by_xpath("//input[@placeholder='Search']")
    searchbar.send_keys(account_name)
    sleep(2)
    searchbar.send_keys(Keys.ENTER)
    sleep(1)
    searchbar.send_keys(Keys.ENTER)
    sleep(4)
    return


def get_connected_accounts(driver, connected_accounts_string):

    follow_button = driver.find_element_by_xpath('//a[contains(@href,{})]'.format(connected_accounts_string))
    original_url = driver.current_url
    follow_button.click()
    sleep(4)



    fBody  = driver.find_element_by_xpath("//div[@class='isgrP']")

    same_count_occurance = 0
    count=0

    #while same_count_occurance < 4:

    for i in range(6):

        # scroll down
        driver.execute_script('arguments[0].scrollTop = arguments[0].scrollTop + arguments[0].offsetHeight;', fBody)

        try:
            sleep(2)
            new_count = len(driver.find_elements_by_xpath("//div[@role='dialog']//li"))
            print('new_count', new_count)
            print('count', count)
            if count == new_count:
                same_count_occurance += 1
            else:
                count = new_count
                same_count_occurance = 0
        except:
            break

    fList  = driver.find_elements_by_xpath("//div[@class='isgrP']//li")
    print("fList len is {}".format(len(fList)))

    try:
        #get tags with a
        hrefs_in_view = driver.find_elements_by_tag_name('a')
        # finding relevant hrefs
        hrefs_in_view = [elem.get_attribute('title') for elem in hrefs_in_view]
        hrefs_in_view = list(filter(lambda x: x != '', hrefs_in_view))
        print(hrefs_in_view)
        print(len(hrefs_in_view))

    except Exception as tag:
        print(tag, "can not find tag")

    driver.get(original_url)

    return hrefs_in_view


def scrape_connected_accounts():

    chrome_options = set_chrome_options()
    driver = webdriver.Chrome(options=chrome_options)
    sleep(2)
    login(driver, os.environ['INSTAGRAM_USERNAME'], os.environ['INSTAGRAM_PASSWORD'])
    navigate_to_account(driver, 'iusedtobeapallet_yyj')

    followers = get_connected_accounts(driver, 'followers')
    following = get_connected_accounts(driver, 'following')

    return followers, following
