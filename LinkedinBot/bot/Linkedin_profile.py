from time import sleep

from .constants import url,username,password
import os
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from selenium.webdriver.common.keys import Keys
from datetime import date
from openpyxl.workbook import Workbook
import urllib.parse

class Linkedin_scraper(webdriver.Chrome):

    @property
    def title(self):
        return self._title

    @property
    def name(self):
        return self._name

    def __init__(self, driver_path=r"C:\Selenium Drivers", teardown=False):
        self.driver_path = driver_path

        self.teardown = teardown
        os.environ["PATH"] += self.driver_path
        # We want to instantiate the webdriver.Chrome class along the way so we use super
        super(Linkedin_scraper, self).__init__()
        self.implicitly_wait(15)
        # Maximize the window
        self.maximize_window()

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.teardown is True:
            self.quit()

    def sign_in(self):
        self.get(url)
        btn = self.find_element(By.LINK_TEXT, "Sign in")
        btn.click()
        username_ele = self.find_element(By.ID, "username")
        username_ele.send_keys(username)
        password_ele = self.find_element(By.ID, "password")
        password_ele.send_keys(password)
        sign_in_btn = self.find_element(By.CSS_SELECTOR, ".from__button--floating")
        sign_in_btn.click()

    def define_attributes(self):
        self.title = []
        self.name = []
        self.profile_link = []
        self.dict = {"Name": self.name, "Title": self.title, "Profile_url": self.profile_link}

    def search(self, search_input):
        self.search_input = search_input
        search_ele = self.find_element(By.CLASS_NAME, "search-global-typeahead__collapsed-search-button")
        input = self.find_element(By.CLASS_NAME, "always-show-placeholder")
        input.send_keys(self.search_input, Keys.ENTER)
        all_results = self.find_element(By.LINK_TEXT, "See all people results")
        all_results.click()

    @title.setter
    def title(self, value):
        self._title = value

    @name.setter
    def name(self, value):
        self._name = value

    def search_results(self):
        scroll = 4
        for i in range(scroll):
            self.find_element(By.TAG_NAME, "html").send_keys(Keys.SPACE)
            sleep(3)
        title = self.find_elements(By.CLASS_NAME, "entity-result__primary-subtitle")
        if len(title) is not None:
            for ele in title:
                self.dict["Title"].append(ele.text)

        # Finding out the name and the profile_link
        name = self.find_elements(By.CLASS_NAME, 'entity-result__title-text')
        j = 0
        for ele in name[0:21:1]:

            linker = ele.find_element(By.TAG_NAME, "a")
            link = linker.get_attribute("href")
            name = ele.find_element(By.CLASS_NAME, "visually-hidden")
            # print(link)
            # print(link)
            # if j == 5:
            #     linker.click()

            self.dict["Profile_url"].append(link)
            name = name.text
            li = name.strip().split(" ")
            str = ""
            str1 = li[2]
            str = str + li[1] + " " + str1[0:len(str1)-2:1]
            # print(str)
            self.dict["Name"].append(str)
            j = j + 1





        # Moving on to the next page
        next_btn = self.find_elements(By.CLASS_NAME, "artdeco-pagination__button--next")
        next_btn = next_btn[0]
        next_btn.click()

    def print_database(self):
        print(self.dict)
        print(len(self.dict["Name"]))
        print(len(self.dict["Title"]))
        print(len(self.dict["Profile_url"]))

    def create_dataframe(self):

        df = pd.DataFrame(self.dict)
        df.to_excel("Maruti_1.xlsx")


