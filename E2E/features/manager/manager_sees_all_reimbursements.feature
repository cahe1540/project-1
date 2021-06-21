Feature: Manager sees all past or pending reimbursements

  Background:
    Given  The guest is on the login page
    When The manager enters username in username input box
    When The manager enters password in password input box
    When The guest clicks the submit button
    Then The manager should be redirected to the manager dashboard

    Scenario: The manager sees pending reimbursements
      Given The manager is logged in
      When The guest clicks on the reimbursement button
      Then The guest should see all reimbursements
      When The manager clicks on the sort status up button
      Then The manager should see pending reimbursements at top of list

    Scenario: The manager sees past reimbursements
      Given The manager is logged in
      When The guest clicks on the reimbursement button
      Then The guest should see all reimbursements
      When The manager clicks on the sort status down button
      Then The manager should see past reimbursements at top of list
