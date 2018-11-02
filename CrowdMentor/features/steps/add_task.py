from behave import given, when, then

@when('I give valid task')
def step_impl(context):
    br = context.browser
    br.visit(context.base_url + '/tasks/add_tasks/')

    # Fill login form and submit it (valid version)
    elem = br.find_by_id('id_task_summary')
    br.find_by_id('id_task_summary').send_keys('Task 1')
    br.find_by_id('id_task_desc').send_keys('Task description')
    #br.find_element_by_id('id_add_task').click()

@then('I am redirected to the task page')
def step_impl(context):
    br = context.browser

    # Checks success status
    assert br.url.endswith('/tasks/add_tasks/')
