import os
import getpass

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.webdriver import WebDriver

from greyt_signer.constant import MOZ_HEADLESS, GREYT_URL


# This will make sure the browser is not opened
os.environ['MOZ_HEADLESS'] = MOZ_HEADLESS

# Setting the firefox driver
DRIVER = webdriver.Firefox()

# Go to greyt page
DRIVER.get(GREYT_URL)

def get_creds():
    """
    Prompt user to enter their greyt username and password
    """

    username = input("username: ")
    password = getpass.getpass("password: ")

    if not username or not password:
        print("username and password not provided")
        exit(0)

    return username, password

def wait_for_page_load(
    driver: WebDriver, catch_key: str, catch_value: str, max_loop_limit: int=None):
    """
    This function job is to wait for the page load.
    """
    count = 0
    while True:

        # This is to insure the loop is only done for a certain period of time
        if max_loop_limit and count >= max_loop_limit:
            print("Max wait time has reached.")
            exit(0)
        
        # Trying to get the element
        try:
            driver.find_element(catch_key, catch_value)
            break
        except:
            pass

def greyt_login(driver: WebDriver) -> WebDriver:
    """
    Login into greyt
    """
    # Get username and password
    username, password = get_creds()

    # Wait for login page to load
    wait_for_page_load(driver, By.ID, "username")

    # Fill the login form value
    driver.find_element(By.ID, "username").send_keys(username)
    driver.find_element(By.ID, "password").send_keys(password)

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
    
    return driver
    

def get_status():
    driver = greyt_login(DRIVER)

    while True:
        try:
            item = driver.execute_script("return document.querySelector('gt-button').shadowRoot.querySelector('button.btn.btn-primary.btn-medium')")
            import time
            time.sleep(10)
            item = driver.execute_script("return document.querySelector('gt-button').shadowRoot.querySelector('button.btn.btn-primary.btn-medium')")
            break
        except:
            pass
    
    if item.text == "Sign In":
        print("You are signed out.")
    elif item.text == "Sign Out":
        print("You are signed in.")
    driver.close()


def entry():
    driver = greyt_login(DRIVER)

    while True:
        try:
            driver.execute_script("return document.querySelector('gt-button').shadowRoot.querySelector('button.btn.btn-primary.btn-medium')")
            import time
            time.sleep(10)
            item = driver.execute_script("return document.querySelector('gt-button').shadowRoot.querySelector('button.btn.btn-primary.btn-medium')")
            break
        except:
            pass
    
    if item.text == "Sign In":
        flag = "Signed In"
    elif item.text == "Sign Out":
        flag = "Signed Out"

    driver.execute_script("document.querySelector('gt-button').shadowRoot.querySelector('button.btn.btn-primary.btn-medium').click()")
    print(flag)

    driver.close()
