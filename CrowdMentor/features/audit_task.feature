Feature: Audit task

  Scenario: Auditor must be able to audit the task
    Given I am an existing user with task updater access
    Given I am an user logged in as the user with task updater access
    And I add a task to be audited
    And I am an existing user with auditor access
    And I am an user logged in as the user with auditor access
