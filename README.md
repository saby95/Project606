# CrowdMentor
Dr.Korok Ray is the director of the Mays Innovation Research Center, and his core area of research is the study of incentive, risk and
reward for human performance. As part of his research, he wants to study how the workers' performance can be improved in a crowdsourcing
environment. The goal of this project is to build a crowdsourcing website which would allow the collection of real world data necessary for
his research.

The website must allow the admins to upload tasks and workers to complete them. Each worker is assigned a
mentor who guides him through the task. The worker earns a salary for each task he completes. Completed tasks are randomly chosen for 
audits and checked for correctness. Based on the audits, the workers either receive a bonus which adds to their salary or a penalty which
subtracts from it. The audits also help evaluate the workers' performance, which helps determine the effectiveness of the training and
incentives being provided to the them. The goal is to build a system where the factors which affect worker performance can be studied
comprehensively.


Iteration 1 : Task Updater(TU) submits the task, Worker completes the task and earns salary.\\
For the first iteration, we can have a simple question answering task where the worker must answer the question.

![](soa_architecture.png)

Requirements(to be converted into user stories):
1) TU must be able to login with privileged access.
2) TU must be able to submit the task i.e the question to be answered.
3) Worker must be be able to login.
4) Worker must be able to locate and accept the task.
5) Worker must be able to complete the task.
6) Worker must earn a salary when he completes the task.
7) Details about the task must be stored in the database.
8) Worker's salary must be displayed in the dashboard.
