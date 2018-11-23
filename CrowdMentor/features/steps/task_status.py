from behave import given, then, when
from django.contrib.auth.models import User
from .users.profile import Profile
from .tasks.models import ResearchTasks, TaskUserJunction

@given('there is a worker')
def step_impl(context):
    u = User(username='Joe')
    u.save()
    context.worker = u

@given('the worker is assigned a task')
def step_impl(context):
    t = ResearchTasks(task_summary='Joe\'s task')
    t.save()
    context.task = t
    tuj = TaskUserJunction(task_id=t, worker_id=context.worker)
    tuj.save()

@given('I am mentoring the worker')
def step_impl(context):
    p = Profile.objects.get(user=context.worker)
    m = User.objects.get(username='mentor')
    p.mentor = m
    p.save()
    context.mentor = m

@then('I can view the status of the worker\'s task')
def step_impl(context):
    br = context.browser
    br.visit(context.base_url + '/tasks/task_status/' + str(context.mentor.id)
             + '/')
    assert br.is_text_present('Joe\'s task')
    assert br.is_text_present('claimed')
