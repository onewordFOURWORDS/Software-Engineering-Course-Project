import pytest
from selenium import webdriver
import sys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from time import sleep
import random
import string
from app import app

def init_driver():
    """
    Initlize a webdriver
    """
    PATH = "/Users/UWIL744/Downloads/chromedriver3"
    driver = webdriver.Chrome(PATH)
    driver.get("http://127.0.0.1:5000/")
    return driver

def submit_form(driver):
    submit = driver.find_element(By.ID, "submit")
    submit.click()


driver = init_driver()
url = driver.current_url