from copy import deepcopy
import datetime
import json
import os
import sqlalchemy
import time

from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys

from app import db, models

from time import sleep, strftime
from random import randint
import pandas as pd


class Scraper(object):

    def __init__(self):

        self.driver = webdriver.Chrome(options = self.set_chrome_options())
        sleep(2)

    def set_chrome_options(self):
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


class InstagramNetworkScraper(Scraper):

    def __init__(self):

        super().__init__()
        self._login(os.environ['INSTAGRAM_USERNAME'], os.environ['INSTAGRAM_PASSWORD'])
        self._home_url = self.driver.current_url


    def _login(self, account_username, account_password):

        self.driver.get('https://www.instagram.com/accounts/login/?source=auth_switcher')

        sleep(3)
        username = self.driver.find_element_by_name('username')
        username.send_keys(account_username)
        password = self.driver.find_element_by_name('password')
        password.send_keys(account_password)
        buttons = self.driver.find_elements_by_tag_name('button')
        login_button = [button for button in buttons if button.text == 'Log In'][0]
        login_button.click()
        sleep(4)
        buttons = self.driver.find_elements_by_tag_name('button')
        not_now_button = [button for button in buttons if button.text == 'Not Now'][0]
        not_now_button.click()
        sleep(4)

        return


    def _navigate_to_account(self, account_name):

        searchbar = self.driver.find_element_by_xpath("//input[@placeholder='Search']")
        searchbar.send_keys(account_name)
        sleep(2)
        searchbar.send_keys(Keys.ENTER)
        sleep(1)
        searchbar.send_keys(Keys.ENTER)
        sleep(4)
        return


    def _get_connected_accounts_list(self, connected_accounts_string):

        follow_button = self.driver.find_element_by_xpath('//a[contains(@href,{})]'.format(connected_accounts_string))
        follow_button.click()
        sleep(4)

        fBody = self.driver.find_element_by_xpath("//div[@class='isgrP']")

        same_count_occurance = 0
        count=0

        #while same_count_occurance < 4:

        for i in range(6):

            # scroll down
            self.driver.execute_script('arguments[0].scrollTop = arguments[0].scrollTop + arguments[0].offsetHeight;', fBody)

            try:
                sleep(2)
                new_count = len(self.driver.find_elements_by_xpath("//div[@role='dialog']//li"))
                print('new_count', new_count)
                print('count', count)
                if count == new_count:
                    same_count_occurance += 1
                else:
                    count = new_count
                    same_count_occurance = 0
            except:
                break

        fList  = self.driver.find_elements_by_xpath("//div[@class='isgrP']//li")
        print("fList len is {}".format(len(fList)))

        try:
            hrefs_in_view = self.driver.find_elements_by_tag_name('a')
            hrefs_in_view = [elem.get_attribute('title') for elem in hrefs_in_view]
            hrefs_in_view = list(filter(lambda x: x != '', hrefs_in_view))
            print(hrefs_in_view)
            print(len(hrefs_in_view))

        except Exception as tag:
            print(tag, "can not find tag")

        self.driver.get(self._home_url)

        return hrefs_in_view


    def scrape_connection_accounts(self, account_name):

        self._navigate_to_account(account_name)

        followers = self._get_connected_accounts_list('followers')
        following = self._get_connected_accounts_list('following')

        return followers, following
