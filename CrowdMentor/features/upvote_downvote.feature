Feature: Workers can upvote and downvote questions and answers

    Scenario: Worker thinks a question is good and wants to upvote it
        Given there exists a question
        And I am an existing user with worker access
        And I am logged in as the user with worker access
        Then I can upvote the question

     Scenario: Worker thinks a question is bad and wants to downvote it
        Given there exists a question
        And I am an existing user with worker access
        And I am logged in as the user with worker access
        Then I can downvote the question
 
    Scenario: Worker thinks an answer is good and wants to upvote it
        Given there exists a question with an answer
        And I am an existing user with worker access
        And I am logged in as the user with worker access
        Then I can upvote the answer
 
    Scenario: Worker thinks an answer is bad and wants to downvote it
        Given there exists a question with an answer
        And I am an existing user with worker access
        And I am logged in as the user with worker access
        Then I can downvote the answer
 
