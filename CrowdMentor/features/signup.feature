Feature: Signup form

  Scenario: Access the signup form

    Given a new user tries to access the site
    When I submit a valid signup page
    Then I am redirected to the home page

    Given a new user tries to access the site
    When I submit an invalid signup page
    Then I get an error message saying that a user with that username already exists.