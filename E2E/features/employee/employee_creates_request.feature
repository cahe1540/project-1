Feature: Employee creates a new reimbursements

  Background:
    Given  The guest is on the login page
    When The guest enters username in username input box
    When The guest enters password in password input box
    When The guest clicks the submit button
    Then The employee should be redirected to the employee dashboard
    When The guest clicks on the myReimbursement button
    Then The guest should see a list of reimbursements
    When The guest clicks on the +new button
    Then The reimbursement submit form should popup
    Then The amount input box should be clear
    Then The reason input box should be clear
    Then The invalid input warning should be hidden

  Scenario: Employee creates a new reimbursement request
    Given The guest is logged in
    When The guest enters the amount into input box
    When  The guest enters the reason into input box
    When  The guest clicks the submit button in the modal
    Then The reimbursement submit form should be hidden
    Then  The new reimbursement should be updated on the reimbursement table
    Then  The success message should display above the reimbursement table
    Then The success message should be hidden
