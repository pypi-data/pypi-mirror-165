import os
import getpass

from selenium import webdriver
from selenium.webdriver.common.by import By


def the_main_function():
    os.environ['MOZ_HEADLESS'] = "1"
    username = input("username: ")
    password = getpass.getpass("password: ")

    if not username or not password:
        print("username and password not provided")
        exit(0)

    driver = webdriver.Firefox()

    # Go to greyt page
    driver.get("https://systango.greythr.com/")

    # Enter the username and password
    while True:
        try:
            driver.find_element(By.ID, "username").send_keys(username)
            driver.find_element(By.ID, "password").send_keys(password)
            break
        except Exception as e:
            pass

    # Click on login button
    try:
        driver.find_element(
            By.XPATH,
            "//button[text()=' Log in ']"
        ).click()
    except Exception as e:
        print("Failed to click on the login button")

    # Wait until we are logged in
    while True:
        try:
            driver.find_element(By.XPATH, "//h1[text()='Home']")
            break
        except Exception as e:
            pass

    while True:
        try:
            item = driver.execute_script("return document.querySelector('gt-button').shadowRoot.querySelector('button.btn.btn-primary.btn-medium')")
            import time
            time.sleep(10)
            item = driver.execute_script("return document.querySelector('gt-button').shadowRoot.querySelector('button.btn.btn-primary.btn-medium')")
            print(item.text)
            break
        except:
            pass
    driver.close()
