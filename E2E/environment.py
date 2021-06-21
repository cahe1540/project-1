from behave.runner import Context
from selenium import webdriver
from poms.app_login_page import AppLoginPage
from poms.manager_dashboard import ManagerDashboard
from poms.employee_dashboard import EmployeeDashboard

import time


def before_all(context: Context):
    context.driver = webdriver.Chrome("C:\\Users\\cahe1\\OneDrive\\Desktop\\chromedriver.exe")
    context.app_login_page = AppLoginPage(context.driver)
    context.employee_dashboard = EmployeeDashboard(context.driver)
    context.manager_dashboard = ManagerDashboard(context.driver)


def after_all(context):
    context.driver.quit()