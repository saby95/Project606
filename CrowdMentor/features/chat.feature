Feature: Chat with Mentor

  Scenario: Existing mentor can send message to his workers
    Given there is one user with worker access
    Given I am an existing user with mentor access mentoring that worker
    Given I am an user logged in as the user with mentor access
    When I send a message to worker
    Then I am redirected to the messages page

  Scenario: Existing worker can send message to his mentor
    Given there is one user with worker access
    Given I am an existing user with mentor access mentoring that worker
    Given I am an user logged in as the user with worker access
    When I send a message to mentor
    Then I am redirected to the messages page
