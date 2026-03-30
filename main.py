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

    print("1. Проверка авторизации")
    driver.get("https://www.saucedemo.com/")
    take_screenshot(driver, "01_login_page")

    driver.find_element(By.ID, "user-name").send_keys("standard_user")
    driver.find_element(By.ID, "password").send_keys("secret_sauce")
    driver.find_element(By.ID, "login-button").click()
    take_screenshot(driver, "02_after_login")

    WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.CLASS_NAME, "inventory_list"))
    )
    assert "inventory.html" in driver.current_url
    print("Авторизация успешна\n")

    print("2. Проверка скролла")
    first_item = WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.CLASS_NAME, "inventory_item"))
    )
    driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", first_item)
    take_screenshot(driver, "03_scroll_to_item")
    print("Скролл выполнен\n")

    print("3. Проверка добавления в корзину")
    driver.find_element(By.CLASS_NAME, "btn_inventory").click()
    take_screenshot(driver, "04_after_add_to_cart")

    cart_badge = driver.find_element(By.CLASS_NAME, "shopping_cart_badge")
    assert cart_badge.text == "1"
    print("Товар добавлен\n")

    print("4. Проверка корзины")
    driver.find_element(By.CLASS_NAME, "shopping_cart_link").click()
    take_screenshot(driver, "05_cart_page")

    WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.CLASS_NAME, "cart_item"))
    )
    print("Корзина содержит товар\n")

    print("5. Проверка оформления заказа")
    driver.find_element(By.ID, "checkout").click()
    take_screenshot(driver, "06_checkout_form")

    driver.find_element(By.ID, "first-name").send_keys("Test")
    driver.find_element(By.ID, "last-name").send_keys("User")
    driver.find_element(By.ID, "postal-code").send_keys("12345")
    take_screenshot(driver, "07_form_filled")
    print("Поля заполнены\n")

    print("6. Проверка завершения покупки")
    driver.find_element(By.ID, "continue").click()
    take_screenshot(driver, "08_after_continue")

    driver.find_element(By.ID, "finish").click()
    take_screenshot(driver, "09_finish")

    success = WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.CLASS_NAME, "complete-header"))
    )
    assert "Thank you for your order" in success.text  # Исправлено с "Done"
    take_screenshot(driver, "10_success")
    print("Заказ успешно оформлен\n")



def test_logout(driver):
    driver.get("https://www.saucedemo.com/")
    driver.find_element(By.ID, "user-name").send_keys("standard_user")
    driver.find_element(By.ID, "password").send_keys("secret_sauce")
    driver.find_element(By.ID, "login-button").click()

    driver.find_element(By.ID, "react-burger-menu-btn").click()
    WebDriverWait(driver, 2).until(
        EC.element_to_be_clickable((By.ID, "logout_sidebar_link"))
    ).click()

    WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.ID, "login-button"))
    )
    assert "saucedemo.com" in driver.current_url
    take_screenshot(driver, "logout_success")


def test_reset_cart(driver):
    driver.get("https://www.saucedemo.com/")
    driver.find_element(By.ID, "user-name").send_keys("standard_user")
    driver.find_element(By.ID, "password").send_keys("secret_sauce")
    driver.find_element(By.ID, "login-button").click()

    driver.find_element(By.CLASS_NAME, "btn_inventory").click()

    driver.find_element(By.ID, "react-burger-menu-btn").click()
    WebDriverWait(driver, 2).until(
        EC.element_to_be_clickable((By.ID, "reset_sidebar_link"))
    ).click()

    cart_badge = driver.find_elements(By.CLASS_NAME, "shopping_cart_badge")
    assert len(cart_badge) == 0
    take_screenshot(driver, "reset_cart_success")