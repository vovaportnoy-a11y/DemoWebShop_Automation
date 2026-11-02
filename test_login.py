import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class TestLogin:
    @pytest.fixture(autouse=True)
    def setup_method(self):
        # Инициализация браузера
        self.driver = webdriver.Chrome()
        self.driver.implicitly_wait(10)
        self.driver.maximize_window()
        yield
        # Закрытие браузера после теста
        self.driver.quit()

    def test_successful_login(self):
        driver = self.driver
        wait = WebDriverWait(driver, 10)

        # 1. Открываем главный сайт
        driver.get("https://demowebshop.tricentis.com/")

        # 2. Переходим к форме логина
        login_link = wait.until(
            EC.element_to_be_clickable((By.CLASS_NAME, "ico-login"))
        )
        login_link.click()

        # 3. Заполняем поля ввода (используем учетные данные зарегистрированного пользователя)
        email_input = wait.until(
            EC.visibility_of_element_located((By.ID, "Email"))
        )
        password_input = driver.find_element(By.ID, "Password")

        # Вставьте здесь email учетной записи
        user_email = "vova.portnoy@gmail.com"
        # ВНИМАНИЕ: Для реальных проектов пароли хранятся в переменной окружения
        user_password = "Talran2026"

        email_input.clear()
        email_input.send_keys(user_email)

        password_input.clear()
        password_input.send_keys(user_password)

        # 4. Нажимаем кнопку входа
        login_button = driver.find_element(By.CSS_SELECTOR, "input.login-button")
        login_button.click()

        # 5. Assert: проверяем успешную авторизацию по отображению email пользователя в шапке
        account_email_element = wait.until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "div.header-links a.account"))
        )

        # Проверяем, что отображаемый текст совпадает с email логина
        assert account_email_element.text == user_email, (
            f"Ожидался email '{user_email}', но отображается '{account_email_element.text}'"
        )

        # Дополнительная проверка: присутствие ссылки Log out
        logout_button = driver.find_element(By.CLASS_NAME, "ico-logout")
        assert logout_button.is_displayed(), "Кнопка 'Log out' не отображается после входа"