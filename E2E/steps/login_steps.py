from behave import given, when, then


@given('The guest is on the login page')
def open_app_login_page(context):
    context.driver.get('C:/Users/cahe1/OneDrive/Documents/revature_training/Projects/project1/login.html')


@when('The guest enters username in username input box')
def enters_user_name(context):
    context.app_login_page.username_input().send_keys('cahe1540')


@when('The guest enters password in password input box')
def enters_password_name(context):
    context.app_login_page.password_input().send_keys('password')


@when('The guest clicks the submit button')
def enters_user_name(context):
    context.app_login_page.submit_btn().click()


@then('The employee should see an error message')
def invalid_login_attempt(context):
    element = context.app_login_page.alert_message()
    assert element.get_attribute('innerHTML') == 'Password or username was incorrect, please try again.'


@then('The employee should be redirected to the employee dashboard')
def is_in_employee_dash(context):
    assert context.employee_dashboard.page_title() == "Employee Dashboard"


@when('The guest enters {username} in username input box')
def enters_user_name(context, username: str):
    context.app_login_page.username_input().send_keys(username)


@when('The guest enters {password} in password input box')
def enters_password(context, password: str):
    context.app_login_page.password_input().send_keys(password)