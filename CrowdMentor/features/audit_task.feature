Feature: Audit task
    In order to make sure that the tasks are being completed correctly,
    the auditor must be able to audit tasks once the worker completes them.

    Scenario: Auditor must be able to audit a task submitted for audit
        Given there is a task to be audited
        Given I am an existing user with auditor access
        And I am logged in as the user with auditor access
        Then I can claim the task for audit
        And I can audit the task
        
