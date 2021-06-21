import time

from behave import given, when, then
from selenium.webdriver.remote.webelement import WebElement


@given('The guest is logged in')
def employee_is_logged_in(context):
    element: WebElement = context.employee_dashboard.nav_hello_message()
    assert element.get_attribute('innerHTML') == 'Welcome,  Carlos!'


@when('The guest clicks on the myReimbursement button')
def click_myReimbursements_button(context):
    time.sleep(.650)  # wait 500ms for fetch to compete
    context.employee_dashboard.myReimbursements_btn().click()


@then('The guest should see a list of reimbursements')
def employee_sees_reimbursements(context):
    element: WebElement = context.employee_dashboard.reimbursement_table()
    assert element


@when('The guest clicks on the sort status up button')
def sort_reimbursement_by_status_desc(context):
    context.employee_dashboard.sort_by_status_up().click()


@then('The guest should see his pending reimbursements at top of list')
def employee_sees_pending_reimbursements(context):
    element: WebElement = context.employee_dashboard.first_table_row()
    assert element.value_of_css_property('background') == "rgb(240, 240, 240) none repeat scroll 0% 0% / auto padding-box border-box"


@when('The guest clicks on the sort status down button')
def sort_reimbursements_by_status_asc(context):
    context.employee_dashboard.sort_by_status_down().click()


@then('The guest should see his past reimbursements at top of list')
def employee_sees_pending_reimbursements(context):
    element: WebElement = context.employee_dashboard.first_table_row()
    assert element.value_of_css_property('background') == "rgb(223, 245, 223) none repeat scroll 0% 0% / auto padding-box border-box"


@when('The guest clicks on the +new button')
def click_new_btn(context):
    context.employee_dashboard.new_btn().click()


@then('The reimbursement submit form should popup')
def check_modal_visible(context):
    element: WebElement = context.employee_dashboard.visible_modal()
    assert element.value_of_css_property('display') != 'None'


@then('The amount input box should be clear')
def amount_input_is_cleared(context):
    element: WebElement = context.employee_dashboard.modal_amount_input()
    assert element.get_attribute('value') == ''


@then('The reason input box should be clear')
def reason_input_is_cleared(context):
    element: WebElement = context.employee_dashboard.modal_reason_input()
    assert element.get_attribute('value') == ''


@then('The invalid input warning should be hidden')
def modal_warn_is_hidden(context):
    element: WebElement = context.employee_dashboard.modal_invalid_warning()
    assert element.get_attribute('class').find('hidden')


@when('The guest clicks on the x button in modal')
def click_x_btn_in_modal(context):
    element: WebElement = context.employee_dashboard.modal_x_btn().click()


@when('The guest clicks on the close button in modal')
def click_x_btn_in_modal(context):
    context.employee_dashboard.modal_close_btn().click()


@then('The reimbursement submit form should be hidden')
def modal_is_hidden(context):
    element: WebElement = context.employee_dashboard.hidden_modal()
    assert element.get_attribute('display') is None


@when('The guest enters the amount into input box')
def add_amount_value(context):
    context.employee_dashboard.modal_amount_input().send_keys('400.00')


@when('The guest enters the reason into input box')
def add_amount_value(context):
    context.employee_dashboard.modal_reason_input().send_keys('refund for fuel?')


@when('The guest clicks the submit button in the modal')
def modal_create_submit_button_pressed(context):
    context.employee_dashboard.modal_submit_btn().click()


@then('The new reimbursement should be updated on the reimbursement table')
def reimbursement_added_to_ui(context):
    last_element_status = context.employee_dashboard.last_row_in_table_status()
    assert last_element_status.get_attribute('innerHTML') == 'pending'


@then('The success message should display above the reimbursement table')
def success_message_displayed(context):
    element: WebElement = context.employee_dashboard.creation_status_visible()
    assert element.get_attribute('class').find('hidden') == -1


@then('The success message should be hidden')
def success_message_hidden(context):
    element: WebElement = context.employee_dashboard.creation_status_hidden()
    assert element.get_attribute('class').find('hidden') >= 0