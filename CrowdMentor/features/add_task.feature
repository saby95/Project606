Feature: Add task form

  Scenario: Access the add task form

    Given an anonymous user
    When I submit a valid login page
    When I give valid task
    Then I am redirected to the task page