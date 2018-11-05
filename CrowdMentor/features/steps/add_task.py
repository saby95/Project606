from behave import given, when, then

@when('I give valid task')
def step_impl(context):
    br = context.browser
    br.visit(context.base_url + '/tasks/add_tasks/')

    # Fill login form and submit it (valid version)
    br.fill('task_desc', 'Task 1')
    print('give valid task: ', br.url)
    br.find_by_id('id_add_task').first.click()

@then('I am redirected to the task page')
def step_impl(context):
    br = context.browser
    #print('give valid task: ', br.url)
    # Checks success status
    assert br.url.endswith('/tasks/')
