Feature: Guest closes a modal

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

  Scenario: Employee closes the submit form popup with the x button
    When The guest clicks on the x button in modal
    Then The reimbursement submit form should be hidden

  Scenario: Employee closes the submit form popup with the close button
    When The guest clicks on the close button in modal
    Then The reimbursement submit form should be hidden
