Feature: Change role form

  Scenario: Access the change role form

    Given I am an admin
    And there is one user with worker access
    And I am logged in as admin
    When I change any user role
    Then I am redirected to the home page