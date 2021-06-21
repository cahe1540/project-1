Feature: A manager logs into the system.

  Scenario Outline: Manager logs in successfully
      Given  The guest is on the login page
      When The guest enters <username> in username input box
      When The guest enters <password> in password input box
      When The guest clicks the submit button
      Then The manager should be redirected to the manager dashboard
       Examples:
    | username | password |
    |    king_henry |   password |
