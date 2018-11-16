from behave import given, when, then
from .tasks.models import ResearchTasks

@given('there is an open task')
def step_impl(context):
    r = ResearchTasks()
    r.save()

@then('I can claim the task')
def step_impl(context):
    br = context.browser
    # When worker clicks the claim button
    br.visit(context.base_url + '/tasks/1/claim')
    # She should be redirected to the tasks page
    assert br.url.endswith('/tasks/')
    assert br.is_text_present('New Task Claimed')

@given('I have claimed a task')
def step_impl(context):
    context.execute_steps(u'there is an open task')
    br = context.browser
    br.visit(context.base_url + '/tasks/1/claim')

@then('I can complete the task')
def step_impl(context):
    pass
