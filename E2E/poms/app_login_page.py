from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait


class AppLoginPage:
    def __init__(self, driver: WebDriver):
        self.driver = driver

    def username_input(self):
        element: WebElement = self.driver.find_element_by_id("userNameInput")
        return element

    def password_input(self):
        element: WebElement = self.driver.find_element_by_id("password")
        return element

    def submit_btn(self):
        element: WebElement = self.driver.find_element_by_class_name("btn")
        return element

    def alert_message(self):
        wait = WebDriverWait(self.driver, 10)
        wait.until(EC.text_to_be_present_in_element((By.CSS_SELECTOR, 'div[role="alert"]'), 'Password or username was incorrect, please try again.'))
        return self.driver.find_element_by_css_selector('div[role="alert"]')
