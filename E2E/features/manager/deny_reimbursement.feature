Feature: Manager denies a reimbursement
  Background:
    Given  The guest is on the login page
    When The manager enters username in username input box
    When The manager enters password in password input box
    When The guest clicks the submit button
    Then The manager should be redirected to the manager dashboard
    When The guest clicks on the reimbursement button
    Then The guest should see all reimbursements
    When The manager clicks on the sort status up button
    Then The manager should see pending reimbursements at top of list

    Scenario: The manager denies a reimbursement
      When The manager clicks on the decide button
      Then A popup should appear
      When The manager adds a comment to the comment box
      When The manager clicks the submit button
      Then The popup should hide
      Then The success message should display above the reimbursement table
      Then The success message should be hidden
      Then The reimbursement list should update for decline