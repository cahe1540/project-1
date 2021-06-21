from behave import given, when, then


@when('The unauthorized guest is in the employee dashboard page')
def protect_employee_dash(context):
    context.driver.get('C:/Users/cahe1/OneDrive/Documents/revature_training/Projects/project1/employee-dash.html')


@when('The unauthorized guest is in the manager dashboard page')
def protect_manager_dash(context):
    context.driver.get('C:/Users/cahe1/OneDrive/Documents/revature_training/Projects/project1/manager-dash.html')


@then('The guest will be redirected to the login page')
def user_was_redirected(context):
    context.driver.title == 'Login'


@when('The guest clicks on the logout button')
def click_logout_btn(context):
    context.employee_dashboard.log_out_btn().click()


@then('The guest should be redirected to the login page')
def redirect_to_login_page(context):
    assert context.driver.title == 'Login'

