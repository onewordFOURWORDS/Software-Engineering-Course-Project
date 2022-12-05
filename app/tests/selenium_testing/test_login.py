from app import app
import pytest
from selenium import webdriver
import sys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from time import sleep
import random
import string


"""
This file is testing the user login page. Issue #1.

Tests cases to validate the acceptance criteria:
    Acceptance: Validate the credentials match a username/password pair in the database.
    Acceptance: Redirect user to homepage after successful login.
"""


def generate_string(size):
    """
    Generates a string of a specified size
    """
    foo = "".join(random.choices(string.ascii_uppercase + string.digits, k=size))
    return foo


def fill_login_form(driver, username: bool, password: bool):
    """
    Fills in the login form with good data

    :param driver: _description_
    :type driver: _type_
    :param username: Fill the username field
    :type username: bool
    :param password: Fill the password field
    :type password: bool
    """
    if username:
        user = driver.find_element(By.ID, "username")
        user.send_keys("username")
    if password:
        password = driver.find_element(By.ID, "password")
        password.send_keys("passpasspass")


def init_driver():
    """
    Initlize a webdriver
    """
    PATH = app.config["SEL_PATH"]
    driver = webdriver.Chrome(PATH)
    driver.get("http://127.0.0.1:5000/login")
    return driver


def submit_form(driver):
    submit = driver.find_element(By.ID, "submit")
    submit.click()


class TestUsernamne:
    def test_username_matching(self):
        """
        Tests that a username entry that matches a database entry is accepted
        """
        driver = init_driver()
        url = driver.current_url

        fill_login_form(driver, username=True, password=True)

        submit_form(driver)
        new_url = driver.current_url

        assert new_url != url

    def test_username_non_matching(self):
        """
        Tests that a username entry that does not matches a database entry is NOT accepted
        """
        driver = init_driver()
        url = driver.current_url

        fill_login_form(driver, username=False, password=True)

        user = driver.find_element(By.ID, "username")
        user.send_keys("no_match" + generate_string(3))

        submit_form(driver)
        new_url = driver.current_url

        assert new_url == url

    def test_username_empty(self):
        """
        Tests that a no username entry is NOT accepted
        """
        driver = init_driver()
        url = driver.current_url

        fill_login_form(driver, username=False, password=True)

        user = driver.find_element(By.ID, "username")
        user.send_keys()

        submit_form(driver)
        new_url = driver.current_url

        assert new_url == url


class TestPassword:
    def test_password_matching(self):
        """
        Tests that a password that matches a database entry is accepted
        """
        driver = init_driver()
        url = driver.current_url

        fill_login_form(driver, username=True, password=True)

        user = driver.find_element(By.ID, "username")
        user.send_keys()

        new_url = driver.current_url

        assert new_url == url
