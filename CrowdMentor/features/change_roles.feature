Feature: Change role form

  Scenario: Access the change role form

    Given an anonymous user
    When I submit a valid login page
    When I change any user role
    Then I am redirected to the home page