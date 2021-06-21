from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait


class EmployeeDashboard:

    def __init__(self, driver: WebDriver):
        self.driver = driver

    def page_title(self):
        wait = WebDriverWait(self.driver, 10)
        wait.until(EC.title_is('Employee Dashboard'))
        return self.driver.title

    def nav_hello_message(self):
        wait = WebDriverWait(self.driver, 10)
        wait.until(EC.text_to_be_present_in_element((By.ID, 'welcome'),
                                                     'Welcome, Carlos!'))
        return self.driver.find_element_by_id('welcome')

    def myReimbursements_btn(self):
        wait = WebDriverWait(self.driver, 10)
        return wait.until(EC.presence_of_element_located((By.ID, 'my-reimbursements')))

    def reimbursement_table(self):
        wait = WebDriverWait(self.driver, 10)
        return wait.until(EC.presence_of_element_located((By.ID, 'my-reimbursement-table')))

    def sort_by_status_up(self):
        wait = WebDriverWait(self.driver, 10)
        return wait.until(EC.presence_of_element_located((By.ID, 'sort-asc')))

    def sort_by_status_down(self):
        wait = WebDriverWait(self.driver, 10)
        return wait.until(EC.presence_of_element_located((By.ID, 'sort-desc')))

    def first_table_row(self):
        wait = WebDriverWait(self.driver, 10)
        return wait.until(EC.presence_of_element_located((By.XPATH, '//table/tbody/tr')))

    def new_btn(self):
        wait = WebDriverWait(self.driver, 10)
        return wait.until(EC.presence_of_element_located((By.ID, 'create-new-btn')))

    def hidden_modal(self):
        wait = WebDriverWait(self.driver, 3)
        wait.until(EC.invisibility_of_element((By.ID, 'exampleModal')))
        return self.driver.find_element_by_id('exampleModal')

    def visible_modal(self):
        wait = WebDriverWait(self.driver, 3)
        wait.until(EC.visibility_of_element_located((By.ID, 'exampleModal')))
        return self.driver.find_element_by_id('exampleModal')

    def modal_amount_input(self):
        wait = WebDriverWait(self.driver, 10)
        return wait.until(EC.element_to_be_clickable((By.ID, 'form-amount')))

    def modal_reason_input(self):
        wait = WebDriverWait(self.driver, 10)
        return wait.until(EC.element_to_be_clickable((By.ID, 'form-reason')))

    def modal_submit_btn(self):
        wait = WebDriverWait(self.driver, 10)
        wait.until(EC.element_to_be_clickable((By.ID, 'submit-my-form')))
        return self.driver.find_element_by_id('submit-my-form')

    def modal_x_btn(self):
        wait = WebDriverWait(self.driver, 10)
        wait.until(EC.element_to_be_clickable((By.ID, 'x-btn')))
        return self.driver.find_element_by_id('x-btn')

    def modal_close_btn(self):
        wait = WebDriverWait(self.driver, 10)
        wait.until(EC.element_to_be_clickable((By.ID, 'modal-close-btn')))
        return self.driver.find_element_by_id('modal-close-btn')

    def modal_invalid_warning(self):
        return self.driver.find_element_by_id('modal-warning')

    def last_row_in_table_status(self):
        wait = WebDriverWait(self.driver, 10)
        wait.until(EC.text_to_be_present_in_element((By.XPATH, '//table/tbody/tr[last()]/td[3]'), 'pending'))
        return self.driver.find_element_by_xpath('//table/tbody/tr[last()]/td[3]')

    def creation_status_visible(self):
        wait = WebDriverWait(self.driver, 10)
        return wait.until(EC.visibility_of_element_located((By.ID, 'creation-alert')))

    def creation_status_hidden(self):
        wait = WebDriverWait(self.driver, 10)
        wait.until(EC.invisibility_of_element_located((By.ID, 'creation-alert')))
        return self.driver.find_element_by_id('creation-alert')

    def log_out_btn(self):
        wait = WebDriverWait(self.driver, 10)
        wait.until(EC.presence_of_element_located((By.ID, 'logout-btn')))
        return self.driver.find_element_by_id('logout-btn')
