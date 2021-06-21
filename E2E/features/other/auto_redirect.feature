Feature: Dashboard pages are protected when no one logged in

  Scenario: No one is logged in so manager and employee pages are protected
    When The unauthorized guest is in the employee dashboard page
    Then The guest will be redirected to the login page
    When The unauthorized guest is in the manager dashboard page
    Then The guest will be redirected to the login page


