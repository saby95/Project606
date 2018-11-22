from .tasks.models import ResearchTasks, Audit
from django.contrib.auth.models import User

@given('I add a task to be audited')
def step_impl(context):
    r = ResearchTasks(audit_prob=1, audit_by=1)
    r.save()

@given('there is a task to be audited')
def step_impl(context):
    context.execute_steps(u'''
    given I am an existing user with task_updater access
    given I am logged in as the user with task_updater access
    and I add a task to be audited
    and I logout
    given I am an existing user with worker access
    given I am logged in as the user with worker access
    then I can claim the task
    then I can complete the task
    given I logout
                          ''')

@then('I can claim the task for audit')
def step_impl(context):
    print(Audit.objects.all())
    r = Audit.objects.get(auditor_id=None).task_id
    br = context.browser
    br.visit(context.base_url + '/tasks/audits/' + str(r.id) + '/claim_audit/')
    assert br.url.endswith('/tasks/audits/')
    assert br.is_text_present('Task Claimed for Review')


@given('I have claimed a task for audit')
def step_impl(context):
    context.execute_steps(u'''
    Then I can claim the task for audit
                          ''')

@then('I can audit the task')
def step_impl(context):
    u = User.objects.get(username='auditor')
    r = Audit.objects.get(auditor_id=u).task_id
    br = context.browser
    br.visit(context.base_url + '/tasks/audits/' + str(r.id) + '/submit_audit')
    br.find_by_id('id_task_correct').first.select('True')
    br.find_by_id('submit').first.click()
    assert br.url.endswith('/tasks/audits/')
    assert br.is_text_present('Review Submitted')
