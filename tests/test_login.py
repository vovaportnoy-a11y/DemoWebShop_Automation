import os
import pytest
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Загружаем логин и пароль из локального файла .env
load_dotenv()
USER_EMAIL = os.getenv("USER_EMAIL")
USER_PASSWORD = os.getenv("USER_PASSWORD")


@pytest.fixture
def driver():
    browser = webdriver.Chrome()
    browser.maximize_window()
    browser.implicitly_wait(10)
    yield browser
    browser.quit()


class TestLogin:

    def test_successful_login(self, driver):
        """Позитивный тест: успешный вход с валидными данными."""
        wait = WebDriverWait(driver, 10)
        driver.get("https://demowebshop.tricentis.com/login")

        email_input = wait.until(EC.visibility_of_element_located((By.ID, "Email")))
        email_input.clear()
        email_input.send_keys(USER_EMAIL)

        password_input = driver.find_element(By.ID, "Password")
        password_input.clear()
        password_input.send_keys(USER_PASSWORD)

        driver.find_element(By.CSS_SELECTOR, "input.login-button").click()

        account_link = wait.until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "div.header-links a.account"))
        )
        assert account_link.text == USER_EMAIL

    def test_login_wrong_password(self, driver):
        """Негативный сценарий 1: зарегистрированный email и неверный пароль."""
        wait = WebDriverWait(driver, 10)
        driver.get("https://demowebshop.tricentis.com/login")

        email_input = wait.until(EC.visibility_of_element_located((By.ID, "Email")))
        email_input.clear()
        email_input.send_keys(USER_EMAIL)

        password_input = driver.find_element(By.ID, "Password")
        password_input.clear()
        password_input.send_keys("WrongPassword999!")

        driver.find_element(By.CSS_SELECTOR, "input.login-button").click()

        error_block = wait.until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "div.validation-summary-errors"))
        )
        assert "The credentials provided are incorrect" in error_block.text
        assert len(driver.find_elements(By.CLASS_NAME, "ico-logout")) == 0

    def test_login_empty_password(self, driver):
        """Негативный сценарий 2: зарегистрированный email и пустой пароль."""
        wait = WebDriverWait(driver, 10)
        driver.get("https://demowebshop.tricentis.com/login")

        email_input = wait.until(EC.visibility_of_element_located((By.ID, "Email")))
        email_input.clear()
        email_input.send_keys(USER_EMAIL)

        password_input = driver.find_element(By.ID, "Password")
        password_input.clear()

        driver.find_element(By.CSS_SELECTOR, "input.login-button").click()

        error_block = wait.until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "div.validation-summary-errors"))
        )
        assert "The credentials provided are incorrect" in error_block.text
        assert len(driver.find_elements(By.CLASS_NAME, "ico-logout")) == 0

    def test_login_invalid_email_format(self, driver):
        """Негативный сценарий 3: некорректный формат email и валидный пароль."""
        wait = WebDriverWait(driver, 10)
        driver.get("https://demowebshop.tricentis.com/login")

        email_input = wait.until(EC.visibility_of_element_located((By.ID, "Email")))
        email_input.clear()
        email_input.send_keys("student.example.com")

        password_input = driver.find_element(By.ID, "Password")
        password_input.clear()
        password_input.send_keys(USER_PASSWORD)

        driver.find_element(By.CSS_SELECTOR, "input.login-button").click()

        field_error = wait.until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "span.field-validation-error"))
        )
        assert field_error.text == "Please enter a valid email address."
        assert len(driver.find_elements(By.CLASS_NAME, "ico-logout")) == 0