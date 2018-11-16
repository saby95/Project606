Feature: Add task form

  Scenario: Access the add task form
    Given I am an existing user with task_updater access
    And I am logged in as the user with task_updater access
    When I give valid task
    Then I am redirected to the task page
