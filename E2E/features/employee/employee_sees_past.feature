Feature: An employee should see pending reimbursements
  Background:
    Given The guest is on the login page
    When The guest enters username in username input box
    When The guest enters password in password input box
    When The guest clicks the submit button

    Scenario: The guest wants to see his past reimbursements
      Given The guest is logged in
      When The guest clicks on the myReimbursement button
      Then The guest should see a list of reimbursements
      When The guest clicks on the sort status down button
      Then The guest should see his past reimbursements at top of list