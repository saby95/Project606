Feature: Audit task

  Background: A task that needs to be audited must exist
    Given there is a task to be audited
    
  Scenario: Auditor must be able to audit the task
    Given I am an existing user with auditor access
    And I am logged in as the user with auditor access
    Then I can claim the task for audit

  Scenario: Auditor can audit a claimed task
    Given I am an existing user with auditor access
    And I am logged in as the user with auditor access
    And I have claimed a task for audit
    Then I can audit the task

