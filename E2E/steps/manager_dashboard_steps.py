import time

from behave import given, when, then
from selenium.webdriver.remote.webelement import WebElement


@when('The manager enters username in username input box')
def enters_user_name(context):
    context.app_login_page.username_input().send_keys('king_henry')


@when('The manager enters password in password input box')
def enters_password_name(context):
    context.app_login_page.password_input().send_keys('password')


@then('The manager should be redirected to the manager dashboard')
def is_in_employee_dash(context):
    assert context.manager_dashboard.page_title() == "Manager Dashboard"


@when('The guest clicks on the reimbursement button')
def click_myReimbursements_button(context):
    time.sleep(.650)  # wait 500ms for fetch to compete
    context.manager_dashboard.reimbursement_btn().click()


@given('The manager is logged in')
def employee_is_logged_in(context):
    element: WebElement = context.manager_dashboard.nav_hello_message()
    assert element.get_attribute('innerHTML') == 'Welcome,  Henry!'


@then('The guest should see all reimbursements')
def employee_sees_reimbursements(context):
    element: WebElement = context.manager_dashboard.reimbursement_table()
    assert element


@when('The manager clicks on the sort status up button')
def sort_reimbursement_by_status_desc(context):
    context.manager_dashboard.sort_by_status_up().click()


@then('The manager should see pending reimbursements at top of list')
def manager_sees_pending_reimbursements(context):
    element: WebElement = context.manager_dashboard.first_table_row_pending()
    assert element.get_attribute('innerHTML') == 'pending'


@when('The manager clicks on the sort status down button')
def sort_reimbursements_by_status_asc(context):
    context.manager_dashboard.sort_by_status_down().click()


@then('The manager should see past reimbursements at top of list')
def manager_sees_past_reimbursements(context):
    element: WebElement = context.manager_dashboard.first_table_row_past()
    assert element.get_attribute('innerHTML') == 'approved' or element.get_attribute('innerHTML') == 'denied'


@when('The guest clicks on the analytics button')
def manager_clicks_analytics_button(context):
    time.sleep(1.4)
    context.manager_dashboard.analytics_btn().click()


@then('The guest should see the charts')
def manager_sees_charts(context):
    element: WebElement = context.manager_dashboard.chart()
    assert element


@when('The manager clicks on the decide button')
def manager_clicks_decide_btn(context):
    element: WebElement = context.manager_dashboard.decide_btn().click()


@when('The manager selects the approve radio button')
def manager_clicks_approve_radio(context):
    element: WebElement = context.manager_dashboard.approve_radio_btn().click()


@then('A popup should appear')
def check_if_pop_up_visible(context):
    element: WebElement = context.manager_dashboard.visible_modal()
    assert element.value_of_css_property('display') != 'None'


@when('The manager adds a comment to the comment box')
def manager_writes_comment(context):
    context.manager_dashboard.comment_text_box().send_keys('Ok, I will approve')


@when('The manager clicks the submit button')
def manager_submits_reimbursement_edit(context):
    context.manager_dashboard.modal_submit_btn().click()


@then('The popup should hide')
def modal_is_hidden(context):
    element: WebElement = context.employee_dashboard.hidden_modal()
    assert element.get_attribute('display') is None


@then('The reimbursement list should update for approval')
def reimbursement_updated_to_ui(context):
    last_element_status = context.manager_dashboard.last_row_approved()
    assert last_element_status.get_attribute('innerHTML') == 'approved'


@then('The reimbursement list should update for decline')
def reimbursement_updated_to_ui(context):
    last_element_status = context.manager_dashboard.last_row_declined()
    assert last_element_status.get_attribute('innerHTML') == 'denied'


@when('async place login username')
def async_login_name(context):
    context.manager_dashboard.async_login_input().send_keys('king_henry')


@when('async place password')
def async_password(context):
    context.manager_dashboard.async_login_password().send_keys('password')


@when('async press submit')
def async_login_btn(context):
    context.manager_dashboard.async_login_submit().click()
