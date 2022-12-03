import pytest
from selenium import webdriver
import sys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from time import sleep
import random
import string
import os
from app import app

"""
This file is testing the user registration page. Issue #15.

Tests cases to validate the acceptance criteria:
    Acceptance: Validate the email does not match an existing email in the database.
    Acceptance: Validate that the entered email structure is correct
    Acceptance: Validate both passwords match and have significant strength.
    Acceptance: Add the user to the database upon successful registration.
    Acceptance: Redirect user to login page after successful registration.
"""


def generate_string(size):
    """
    Generates a string of a specified size
    """
    foo = "".join(random.choices(string.ascii_uppercase + string.digits, k=size))
    return foo


def fill_registration_form(
    driver, username: bool, email: bool, firstname: bool, lastname: bool, password: bool
):
    """
    Fills all the True fields with valid data

    :param driver: ChromeDriver
    :type driver: _type_
    :param username: Fill the username field
    :type username: bool
    :param email: Fill the email field
    :type email: bool
    :param firstname: Fill the firstname field
    :type firstname: bool
    :param lastname: Fill the lastname field
    :type lastname: bool
    :param password: Fill the password fields
    :type password: bool
    """
    if username:
        user = driver.find_element(By.ID, "username")
        user.send_keys(generate_string(6))
    if email:
        email = driver.find_element(By.ID, "email")
        email.send_keys(generate_string(5) + "@email.com")
    if firstname:
        fname = driver.find_element(By.ID, "first_name")
        fname.send_keys(generate_string(10))
    if lastname:
        lname = driver.find_element(By.ID, "last_name")
        lname.send_keys(generate_string(10))
    if password:
        rpass = generate_string(12)

        pass1 = driver.find_element(By.ID, "password")
        pass1.send_keys(rpass)

        pass2 = driver.find_element(By.ID, "password2")
        pass2.send_keys(rpass)


def init_driver():
    """
    Initlize a webdriver
    """
    PATH = app.config["SEL_PATH"]
    driver = webdriver.Chrome(PATH)
    driver.get("http://127.0.0.1:5000/register")
    return driver


def submit_form(driver):
    submit = driver.find_element(By.ID, "submit")
    submit.click()


class TestUsername:
    def test_username_under(self):
        """
        Tests that a username below lower bound does NOT work
        """
        driver = init_driver()
        url = driver.current_url

        fill_registration_form(
            driver,
            username=False,
            email=True,
            firstname=True,
            lastname=True,
            password=True,
        )

        user = driver.find_element(By.ID, "username")
        user.send_keys(generate_string(2))

        submit_form(driver)
        new_url = driver.current_url

        assert new_url == url

    def test_username_lower(self):
        """
        Tests that a username of lengthlower bound works
        """
        driver = init_driver()
        url = driver.current_url

        fill_registration_form(
            driver,
            username=False,
            email=True,
            firstname=True,
            lastname=True,
            password=True,
        )

        user = driver.find_element(By.ID, "username")
        user.send_keys(generate_string(3))

        submit_form(driver)
        new_url = driver.current_url

        assert new_url != url

    def test_username_upper(self):
        """
        Tests that a username of length upper bound works
        """
        driver = init_driver()
        url = driver.current_url

        fill_registration_form(
            driver,
            username=False,
            email=True,
            firstname=True,
            lastname=True,
            password=True,
        )

        user = driver.find_element(By.ID, "username")
        user.send_keys(generate_string(32))

        submit_form(driver)
        new_url = driver.current_url

        assert new_url != url

    def test_username_over(self):
        """
        Tests that a username of length over the upper bound does NOT work
        """
        driver = init_driver()
        url = driver.current_url

        fill_registration_form(
            driver,
            username=False,
            email=True,
            firstname=True,
            lastname=True,
            password=True,
        )

        user = driver.find_element(By.ID, "username")
        user.send_keys(generate_string(33))

        submit_form(driver)
        new_url = driver.current_url

        assert new_url == url

    def test_username_empty(self):
        """
        Tests that a username of no input is NOT accepted
        """
        driver = init_driver()
        url = driver.current_url

        fill_registration_form(
            driver,
            username=False,
            email=True,
            firstname=True,
            lastname=True,
            password=True,
        )

        user = driver.find_element(By.ID, "username")
        user.send_keys()

        submit_form(driver)
        new_url = driver.current_url

        assert new_url == url

    def test_username_duplicate(self):
        """
        Tests that a duplicated username is NOT accepted
        """
        driver = init_driver()
        url = driver.current_url

        fill_registration_form(
            driver,
            username=False,
            email=True,
            firstname=True,
            lastname=True,
            password=True,
        )

        user = driver.find_element(By.ID, "username")
        user.send_keys("username")

        submit_form
        new_url = driver.current_url

        assert new_url == url


class TestEmail:
    def test_email_correct_format(self):
        """
        Tests that an email of format <string>@<string>.<string> is accepted
        """
        driver = init_driver()
        url = driver.current_url

        fill_registration_form(
            driver,
            username=True,
            email=False,
            firstname=True,
            lastname=True,
            password=True,
        )

        email = driver.find_element(By.ID, "email")
        email.send_keys(generate_string(5) + "@email.com")

        submit_form(driver)
        new_url = driver.current_url

        assert new_url != url

    def test_email_incorrect_format(self):
        """
        Tests that an email of format <string>@<string> is NOT accepted
        """
        driver = init_driver()
        url = driver.current_url

        fill_registration_form(
            driver,
            username=True,
            email=False,
            firstname=True,
            lastname=True,
            password=True,
        )

        email = driver.find_element(By.ID, "email")
        email.send_keys(generate_string(5) + "@" + generate_string(3))

        submit_form(driver)
        new_url = driver.current_url

        assert new_url == url

    def test_email_no_input(self):
        """
        Tests that an email of no input is NOT accepted
        """
        driver = init_driver()
        url = driver.current_url

        fill_registration_form(
            driver,
            username=True,
            email=False,
            firstname=True,
            lastname=True,
            password=True,
        )

        email = driver.find_element(By.ID, "email")
        email.send_keys()

        submit_form(driver)
        new_url = driver.current_url

        assert new_url == url

    def test_email_duplicate(self):
        """
        Tests that an email of no input is NOT accepted
        """
        driver = init_driver()
        url = driver.current_url

        fill_registration_form(
            driver,
            username=True,
            email=False,
            firstname=True,
            lastname=True,
            password=True,
        )

        email = driver.find_element(By.ID, "email")
        email.send_keys("email@email.com")

        submit_form(driver)
        new_url = driver.current_url

        assert new_url == url


class TestFirstName:
    def test_firstname_string(self):
        """
        Tests that a string is accepted
        """
        driver = init_driver()
        url = driver.current_url

        fill_registration_form(
            driver,
            username=True,
            email=True,
            firstname=False,
            lastname=True,
            password=True,
        )

        fname = driver.find_element(By.ID, "first_name")
        fname.send_keys(generate_string(10))

        submit_form(driver)
        new_url = driver.current_url

        assert new_url != url

    def test_firstname_no_input(self):
        """
        Tests that no input is NOT accepted
        """
        driver = init_driver()
        url = driver.current_url

        fill_registration_form(
            driver,
            username=True,
            email=True,
            firstname=False,
            lastname=True,
            password=True,
        )

        fname = driver.find_element(By.ID, "first_name")
        fname.send_keys()

        submit_form(driver)
        new_url = driver.current_url

        assert new_url == url


class TestLastName:
    def test_lastname_string(self):
        """
        Tests that a string is accepted
        """
        driver = init_driver()
        url = driver.current_url

        fill_registration_form(
            driver,
            username=True,
            email=True,
            firstname=True,
            lastname=False,
            password=True,
        )

        lname = driver.find_element(By.ID, "last_name")
        lname.send_keys(generate_string(10))

        submit_form(driver)
        new_url = driver.current_url

        assert new_url != url

    def test_lastname_no_input(self):
        """
        Tests that  no input is NOT accepted
        """
        driver = init_driver()
        url = driver.current_url

        fill_registration_form(
            driver,
            username=True,
            email=True,
            firstname=True,
            lastname=False,
            password=True,
        )

        lname = driver.find_element(By.ID, "last_name")
        lname.send_keys()

        submit_form(driver)
        new_url = driver.current_url

        assert new_url == url


class TestPassword:
    def test_password_under(self):
        """
        Tests that a password length under min is NOT accepted
        """
        driver = init_driver()
        url = driver.current_url

        fill_registration_form(
            driver,
            username=True,
            email=True,
            firstname=True,
            lastname=True,
            password=False,
        )

        rpass = generate_string(11)

        pass1 = driver.find_element(By.ID, "password")
        pass1.send_keys(rpass)

        pass2 = driver.find_element(By.ID, "password2")
        pass2.send_keys(rpass)

        submit_form(driver)
        new_url = driver.current_url

        assert new_url == url

    def test_password_lower(self):
        """
        Tests that a password length min is accepted
        """
        driver = init_driver()
        url = driver.current_url

        fill_registration_form(
            driver,
            username=True,
            email=True,
            firstname=True,
            lastname=True,
            password=False,
        )

        rpass = generate_string(12)

        pass1 = driver.find_element(By.ID, "password")
        pass1.send_keys(rpass)

        pass2 = driver.find_element(By.ID, "password2")
        pass2.send_keys(rpass)

        submit_form(driver)
        new_url = driver.current_url

        assert new_url != url

    def test_password_upper(self):
        """
        Tests that a password length max is accepted
        """
        driver = init_driver()
        url = driver.current_url

        fill_registration_form(
            driver,
            username=True,
            email=True,
            firstname=True,
            lastname=True,
            password=False,
        )

        rpass = generate_string(64)

        pass1 = driver.find_element(By.ID, "password")
        pass1.send_keys(rpass)

        pass2 = driver.find_element(By.ID, "password2")
        pass2.send_keys(rpass)

        submit_form(driver)
        new_url = driver.current_url

        assert new_url != url

    def test_password_over(self):
        """
        Tests that a password over the max is NOT accepted
        """
        driver = init_driver()
        url = driver.current_url

        fill_registration_form(
            driver,
            username=True,
            email=True,
            firstname=True,
            lastname=True,
            password=False,
        )

        rpass = generate_string(65)

        pass1 = driver.find_element(By.ID, "password")
        pass1.send_keys(rpass)

        pass2 = driver.find_element(By.ID, "password2")
        pass2.send_keys(rpass)

        submit_form(driver)
        new_url = driver.current_url

        assert new_url == url

    def test_password_empty(self):
        """
        Tests that a no input is NOT accepted
        """
        driver = init_driver()
        url = driver.current_url

        fill_registration_form(
            driver,
            username=True,
            email=True,
            firstname=True,
            lastname=True,
            password=False,
        )

        rpass = ""

        pass1 = driver.find_element(By.ID, "password")
        pass1.send_keys(rpass)

        pass2 = driver.find_element(By.ID, "password2")
        pass2.send_keys(rpass)

        submit_form(driver)
        new_url = driver.current_url

        assert new_url == url

    def test_password_non_match(self):
        """
        Tests that a two different passwords are NOT accepted
        """
        driver = init_driver()
        url = driver.current_url

        fill_registration_form(
            driver,
            username=True,
            email=True,
            firstname=True,
            lastname=True,
            password=False,
        )

        rpass = generate_string(11)
        rpass2 = generate_string(11)

        pass1 = driver.find_element(By.ID, "password")
        pass1.send_keys(rpass)

        pass2 = driver.find_element(By.ID, "password2")
        pass2.send_keys(rpass2)

        submit_form(driver)
        new_url = driver.current_url

        assert new_url == url
