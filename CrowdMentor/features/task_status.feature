Feature: View task status
    An admin should be able to view the status of all tasks
    A mentor should be able to view the status of tasks assigned to the
    workers being mentored by her.

Scenario: A mentor should be able to see her workers' task status 

    Given there is a worker
    And the worker is assigned a task
    And I am an existing user with mentor access
    And I am logged in as the user with mentor access
    And I am mentoring the worker
    Then I can view the status of the worker's task
