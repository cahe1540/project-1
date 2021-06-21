Feature: Guest logs out

Background:
    Given  The guest is on the login page
    When The guest enters username in username input box
    When The guest enters password in password input box
    When The guest clicks the submit button
    Then The employee should be redirected to the employee dashboard

  Scenario: The guest logs out
    Given The guest is logged in
    When The guest clicks on the logout button
    Then The guest should be redirected to the login page