Feature: Manager sees analytics

  Background:
    Given The guest is on the login page
    When The manager enters username in username input box
    When The manager enters password in password input box
    When The guest clicks the submit button
    Then The manager should be redirected to the manager dashboard

    Scenario: Manager goes to analytics page
      Given The manager is logged in
      When The guest clicks on the analytics button
      Then The guest should see the charts