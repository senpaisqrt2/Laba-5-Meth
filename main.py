import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.firefox import GeckoDriverManager
import os
from datetime import datetime


@pytest.fixture
def driver():
    # Настройки Firefox
    options = Options()
    options.add_argument("--width=1920")
    options.add_argument("--height=1080")

    # Автоматическая установка geckodriver
    service = Service(GeckoDriverManager().install())
    driver = webdriver.Firefox(service=service, options=options)

    yield driver
    driver.quit()


def take_screenshot(driver, name):
    """Функция для скриншота"""
    if not os.path.exists("screenshots"):
        os.makedirs("screenshots")
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"screenshots/firefox_{name}_{timestamp}.png"
    driver.save_screenshot(filename)
    print(f"Скриншот сохранён: {filename}")


def test_smoke_saucedemo_firefox(driver):
    """Дымовое тестирование saucedemo.com в Firefox"""

    print("\n=== НАЧАЛО ДЫМОВОГО ТЕСТИРОВАНИЯ ===\n")

    # 1. Открыть сервис
    driver.get("https://www.saucedemo.com/")
    take_screenshot(driver, "01_login_page")
    print("✓ Открыта страница логина")

    # 2. Заполнение полей ввода
    username_field = driver.find_element(By.ID, "user-name")
    username_field.send_keys("standard_user")
    print("✓ Заполнено поле username")

    password_field = driver.find_element(By.ID, "password")
    password_field.send_keys("secret_sauce")
    print("✓ Заполнено поле password")

    # 3. Нажатие кнопки
    login_button = driver.find_element(By.ID, "login-button")
    login_button.click()
    print("✓ Нажата кнопка Login")
    take_screenshot(driver, "02_after_login")

    # 4. Ожидание загрузки страницы
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "inventory_item"))
    )
    print("✓ Страница инвентаря загружена")

    # 5. Скролл до первого товара (по локатору)
    first_item = driver.find_element(By.CLASS_NAME, "inventory_item")
    driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", first_item)
    print("✓ Выполнен скролл до первого товара")
    take_screenshot(driver, "03_scroll_to_item")

    # 6. Добавление товара в корзину
    add_button = driver.find_element(By.CLASS_NAME, "btn_inventory")
    add_button.click()
    print("✓ Товар добавлен в корзину")
    take_screenshot(driver, "04_added_to_cart")

    # 7. Скролл до корзины и переход
    cart_icon = driver.find_element(By.CLASS_NAME, "shopping_cart_link")
    driver.execute_script("arguments[0].scrollIntoView();", cart_icon)
    cart_icon.click()
    print("✓ Переход в корзину")
    take_screenshot(driver, "05_cart_page")

    # 8. Нажатие Checkout
    checkout_button = driver.find_element(By.ID, "checkout")
    driver.execute_script("arguments[0].scrollIntoView();", checkout_button)
    checkout_button.click()
    print("✓ Нажата кнопка Checkout")
    take_screenshot(driver, "06_checkout_step_one")

    # 9. Заполнение формы оформления
    driver.find_element(By.ID, "first-name").send_keys("Ivan")
    driver.find_element(By.ID, "last-name").send_keys("Petrov")
    driver.find_element(By.ID, "postal-code").send_keys("101000")
    print("✓ Заполнены данные заказа")
    take_screenshot(driver, "07_checkout_form_filled")

    # 10. Скролл до кнопки Continue и нажатие
    continue_btn = driver.find_element(By.ID, "continue")
    driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", continue_btn)
    continue_btn.click()
    print("✓ Нажата кнопка Continue")
    take_screenshot(driver, "08_after_continue")

    # 11. Скролл до кнопки Finish и завершение
    finish_btn = driver.find_element(By.ID, "finish")
    driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", finish_btn)
    finish_btn.click()
    print("✓ Нажата кнопка Finish")
    take_screenshot(driver, "09_finish")

    # 12. Проверка успешного завершения
    success_msg = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "complete-header"))
    )
    assert "Thank you for your order" in success_msg.text
    print("✓ Заказ успешно оформлен!")
    take_screenshot(driver, "10_success")

    print("\n=== ДЫМОВОЕ ТЕСТИРОВАНИЕ УСПЕШНО ЗАВЕРШЕНО ===\n")


# Дополнительный тест для демонстрации разных локаторов
def test_scroll_by_different_locators(driver):
    """Пример скролла по разным типам локаторов"""
    driver.get("https://www.saucedemo.com/")

    # Логин
    driver.find_element(By.ID, "user-name").send_keys("standard_user")
    driver.find_element(By.ID, "password").send_keys("secret_sauce")
    driver.find_element(By.ID, "login-button").click()

    WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.CLASS_NAME, "inventory_list"))
    )

    # Скролл по CSS селектору
    element_by_css = driver.find_element(By.CSS_SELECTOR, ".inventory_item:last-child")
    driver.execute_script("arguments[0].scrollIntoView();", element_by_css)
    take_screenshot(driver, "scroll_by_css")

    # Скролл по XPATH
    element_by_xpath = driver.find_element(By.XPATH, "//button[contains(text(), 'Add to cart')]")
    driver.execute_script("arguments[0].scrollIntoView();", element_by_xpath)
    take_screenshot(driver, "scroll_by_xpath")

    # Скролл по тексту ссылки
    element_by_link = driver.find_element(By.LINK_TEXT, "Twitter")
    driver.execute_script("arguments[0].scrollIntoView();", element_by_link)
    take_screenshot(driver, "scroll_by_link_text")

    print("✓ Все типы скроллов выполнены успешно")