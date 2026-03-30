import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
from datetime import datetime


@pytest.fixture
def driver():
    options = Options()
    options.add_argument("--width=1920")
    options.add_argument("--height=1080")

    service = Service(executable_path=r"C:\Users\senpai_sqrt2\Downloads\geckodriver-v0.36.0-win64\geckodriver.exe")

    driver = webdriver.Firefox(service=service, options=options)
    yield driver
    driver.quit()

def take_screenshot(driver, name):
    if not os.path.exists("screenshots"):
        os.makedirs("screenshots")
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"screenshots/{name}_{timestamp}.png"
    driver.save_screenshot(filename)
    print(f"Скриншот: {filename}")


def test_smoke(driver):
    driver.get("https://www.saucedemo.com/")
    take_screenshot(driver, "01_start")

    driver.find_element(By.ID, "user-name").send_keys("standard_user")
    driver.find_element(By.ID, "password").send_keys("secret_sauce")
    driver.find_element(By.ID, "login-button").click()
    take_screenshot(driver, "02_login")

    first_item = WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.CLASS_NAME, "inventory_item"))
    )
    driver.execute_script("arguments[0].scrollIntoView();", first_item)
    take_screenshot(driver, "03_scroll")

    driver.find_element(By.CLASS_NAME, "btn_inventory").click()
    driver.find_element(By.CLASS_NAME, "shopping_cart_link").click()
    take_screenshot(driver, "04_cart")

    driver.find_element(By.ID, "checkout").click()
    driver.find_element(By.ID, "first-name").send_keys("Test")
    driver.find_element(By.ID, "last-name").send_keys("User")
    driver.find_element(By.ID, "postal-code").send_keys("12345")
    driver.find_element(By.ID, "continue").click()
    driver.find_element(By.ID, "finish").click()
    take_screenshot(driver, "05_finish")

    success = WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.CLASS_NAME, "complete-header"))
    )
    assert "Done" in success.text