from selenium.common import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait


class LoginPage:

    LOGIN_LINK = (By.CSS_SELECTOR, "a[href='/login']")
    EMAIL_INPUT = (By.CSS_SELECTOR,"input[name='email']")
    PASSWORD_INPUT = (By.CSS_SELECTOR,"input[name='password']")
    BUTTON = (By.CSS_SELECTOR,"button[name='login']")
    SIGN_OUT_BUTTON = (By.XPATH, "//*[text()='Sign Out']")

    def __init__(self, driver):
        self.driver = driver

    def open_login_page(self):
        self.driver.find_element(*self.LOGIN_LINK).click()

    def fill_email_field(self, email):
        self.driver.find_element(*self.EMAIL_INPUT).clear()
        self.driver.find_element(*self.EMAIL_INPUT).send_keys(email)

    def fill_password_field(self, password):
        self.driver.find_element(*self.PASSWORD_INPUT).clear()
        self.driver.find_element(*self.PASSWORD_INPUT).send_keys(password)

    def click_on_login_button(self):
        self.driver.find_element(*self.BUTTON).click()

    # def is_sign_out_displayed(self):
    #     return self.driver.find_element(*self.SIGN_OUT_BUTTON).is_displayed()

    def is_sign_out_displayed(self):
        try:
            WebDriverWait(self.driver, timeout=10).until(
                expected_conditions.visibility_of_element_located(self.SIGN_OUT_BUTTON)
            )
            return True
        except TimeoutException:
            return False
