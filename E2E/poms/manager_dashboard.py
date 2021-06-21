import re

from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait


class ManagerDashboard:
    def __init__(self, driver: WebDriver):
        self.driver = driver

    def page_title(self):
        wait = WebDriverWait(self.driver, 10)
        wait.until(EC.title_is('Manager Dashboard'))
        return self.driver.title

    def reimbursement_btn(self):
        wait = WebDriverWait(self.driver, 10)
        return wait.until(EC.presence_of_element_located((By.ID, 'reimbursements')))

    def reimbursement_table(self):
        wait = WebDriverWait(self.driver, 10)
        return wait.until(EC.presence_of_element_located((By.ID, 'reimbursement-table')))

    def nav_hello_message(self):
        wait = WebDriverWait(self.driver, 10)
        wait.until(EC.text_to_be_present_in_element((By.ID, 'welcome'),
                                                    'Welcome, Henry!'))
        return self.driver.find_element_by_id('welcome')

    def sort_by_status_up(self):
        wait = WebDriverWait(self.driver, 10)
        return wait.until(EC.presence_of_element_located((By.ID, 'sort-asc')))

    def first_table_row_pending(self):
        wait = WebDriverWait(self.driver, 10)
        wait.until(EC.text_to_be_present_in_element((By.XPATH, '//table/tbody/tr/td[4]'), 'pending'))
        return self.driver.find_element_by_xpath('//table/tbody/tr/td[4]')

    def first_table_row_past(self):
        wait = WebDriverWait(self.driver, 10)
        wait.until(EC.text_to_be_present_in_element((By.XPATH, '//table/tbody/tr/td[4]'), 'approved'))
        return self.driver.find_element_by_xpath('//table/tbody/tr/td[4]')

    def sort_by_status_down(self):
        wait = WebDriverWait(self.driver, 10)
        return wait.until(EC.presence_of_element_located((By.ID, 'sort-desc')))

    def analytics_btn(self):
        wait = WebDriverWait(self.driver, 10)
        return wait.until(EC.presence_of_element_located((By.ID, 'analytics')))

    def chart(self):
        wait = WebDriverWait(self.driver, 10)
        return wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div[aria-label="A chart."]')))

    def decide_btn(self):
        wait = WebDriverWait(self.driver, 10)
        return wait.until(EC.presence_of_element_located((By.ID, 'update-btn')))

    def approve_radio_btn(self):
        wait = WebDriverWait(self.driver, 10)
        return wait.until(EC.element_to_be_clickable((By.ID, 'radio-approve')))

    def comment_text_box(self):
        wait = WebDriverWait(self.driver, 10)
        return wait.until(EC.element_to_be_clickable((By.ID, 'form-message')))

    def visible_modal(self):
        wait = WebDriverWait(self.driver, 10)
        wait.until(EC.visibility_of_element_located((By.ID, 'exampleModal')))
        return self.driver.find_element_by_id('exampleModal')

    def hidden_modal(self):
        wait = WebDriverWait(self.driver, 10)
        wait.until(EC.invisibility_of_element((By.ID, 'exampleModal')))
        return self.driver.find_element_by_id('exampleModal')

    def modal_submit_btn(self):
        wait = WebDriverWait(self.driver, 10)
        wait.until(EC.element_to_be_clickable((By.ID, 'submit-my-form')))
        return self.driver.find_element_by_id('submit-my-form')

    def last_row_approved(self):
        wait = WebDriverWait(self.driver, 10)
        wait.until(EC.text_to_be_present_in_element((By.XPATH, '//table/tbody/tr[last()]/td[4]'), 'approved'))
        return self.driver.find_element_by_xpath('//table/tbody/tr[last()]/td[4]')

    def last_row_declined(self):
        wait = WebDriverWait(self.driver, 10)
        wait.until(EC.text_to_be_present_in_element((By.XPATH, '//table/tbody/tr[last()]/td[4]'), 'denied'))
        return self.driver.find_element_by_xpath('//table/tbody/tr[last()]/td[4]')
