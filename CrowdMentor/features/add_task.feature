Feature: Add task form

  Scenario: Access the add task form
    Given I am an existing user with task updater access
    Given I am an user logged in as the user with task updater access
    When I give valid task
    Then I am redirected to the task page