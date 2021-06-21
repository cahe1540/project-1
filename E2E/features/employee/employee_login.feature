Feature: A user logs into the employee dashboard

  Scenario Outline: Employee logs in with invalid credentials
    Given  The guest is on the login page
    When The guest enters <username> in username input box
    When The guest enters <password> in password input box
    When The guest clicks the submit button
    Then The employee should see an error message
    Examples:
    | username | password |
    |    adfa31 |   password |
    |    cahe1540 |   passwordfda |
    |      dfa    |       daa  |

  Scenario: Employee logs in successfully
    Given  The guest is on the login page
    When The guest enters username in username input box
    When The guest enters password in password input box
    When The guest clicks the submit button
    Then The employee should be redirected to the employee dashboard
