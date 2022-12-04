import pytest
from selenium import webdriver
import sys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from time import sleep
import random
import string
from datetime import datetime

# Tests written by David Williams

def init_driver():
    """
    Initlize a webdriver
    """
    PATH = "/Users/UWIL744/Downloads/chromedriver3"
    driver = webdriver.Chrome(PATH)
    return driver

def login_to_create_tournament(driver):
    driver.get("http://127.0.0.1:5000/login")
    user = driver.find_element(By.ID, "username")
    user.send_keys("david")
    password = driver.find_element(By.ID, "password")
    password.send_keys("12345678")
    submit_form(driver)
    driver.find_element(By.ID, "create_tournament_link").click()


def fill_tournament_form(driver, name, city, tournament_state, tournament_league, date):
    tournament_name = driver.find_element(By.ID, "tournament_name")
    tournament_name.send_keys(name)
    tournament_city = driver.find_element(By.ID, "tournament_city")
    tournament_city.send_keys(city)
    select = Select(driver.find_element(By.NAME, 'state'))
    select.select_by_value(tournament_state)
    league_name = driver.find_element(By.ID, "tournament_league")
    league_name.send_keys(tournament_league)
    driver.find_element(By.ID, "tournament_date").click()
    submit_form(driver)


def submit_form(driver):
    submit = driver.find_element(By.ID, "submit")
    submit.click()


def test_tournament_name_matching():
    """
    Tests that a tournament name entry that matches a database entry is accepted
    """
    driver = init_driver()
    url = driver.current_url

    login_to_create_tournament(driver)
    fill_tournament_form(driver,"Test Tournament", "test city", "NC", 1, datetime.utcnow)

    submit_form(driver)
    new_url = driver.current_url

    assert new_url != url

def test_tournament_name_as_symbol():
    """
    Tests that a tournament name entry that matches a database entry is accepted
    """
    driver = init_driver()
    url = driver.current_url

    login_to_create_tournament(driver)
    fill_tournament_form(driver,"%", "test city", "NC", 1, datetime.utcnow)

    submit_form(driver)
    new_url = driver.current_url

    assert new_url == url



