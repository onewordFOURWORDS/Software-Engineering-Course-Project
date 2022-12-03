import pytest
from selenium import webdriver
from app import app
import sys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from time import sleep
import random
import string
from app.models import Tournament

"""
This file is testing the tournament searching functionality on the tournament dashboard page. Issues #2 and #28.

Tests cases to validate the acceptance criteria:
    Acceptance: The user is shown a list of tournaments within the specified date range. (#2)
    Acceptance: The user is shown a list of tournaments with exact and partial name matches. (#28)
    Acceptance: The user is shown an error message when no matches are found. (#28)
"""


def generate_string(size):
    """
    Generates a string of a specified size
    """
    foo = "".join(random.choices(string.ascii_uppercase + string.digits, k=size))
    return foo


def fill_search_form(driver, name: bool):
    """
    Fills in the search form with good data

    :param driver: Chromedriver
    :type driver: _type_
    :param name: Fill the name field
    :type name: bool
    """
    if name:
        name_field = driver.find_element(By.ID, "name_field")
        name_field.send_keys("tournament 1")


def init_driver():
    """
    Initlize a webdriver
    """
    PATH = app.config["SEL_PATH"]
    driver = webdriver.Chrome(PATH)
    driver.get("http://127.0.0.1:5000/tournament_dashboard")
    return driver


def submit_form(driver):
    submit = driver.find_element(By.ID, "submit")
    submit.click()


class TestTournamentName:
    def test_name_matching(self):
        """
        Tests that a tournament name entry that matches a database entry displays that tournament
        """
        driver = init_driver()

        fill_search_form(driver, name=True)

        submit_form(driver)

        returned = driver.find_element(By.CLASS_NAME, "tournament")

        assert returned != "NoSuchElementException", f'Expected "tournament 1", got: {returned}'

    def test_name_non_matching(self):
        """
        Tests that a tournament name entry that does not match a database entry displays nothing
        """
        driver = init_driver()

        fill_search_form(driver, name=False)

        name_field = driver.find_element(By.ID, "name_field")
        name_field.send_keys("no match")

        submit_form(driver)

        # throws NoSuchElementException if no element is found
        returned = driver.find_element(By.CLASS_NAME, "tournament")

        assert returned == "NoSuchElementException", f"Expected no tournament, got: {returned}"

    def test_name_empty(self):
        """
        Tests that no tournament name provided displays all tournaments
        """
        driver = init_driver()

        fill_search_form(driver, name=False)

        name_field = driver.find_element(By.ID, "name_field")
        name_field.send_keys()

        submit_form(driver)

        # pull all tournaments in database and compare if that array is equal to the one returned
        displayed = driver.find_elements(By.CLASS_NAME, "tournament")
        database = Tournament.query.all()

        assert displayed == database, f"Expected all tournaments, got: {displayed}"
