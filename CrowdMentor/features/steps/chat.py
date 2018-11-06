from behave import given, when, then

@when('I send a message to worker')
def step_impl(context):
    br = context.browser
    br.visit(context.base_url + '/messages/')
    br.fill('message', 'Hello Worker')
    br.find_by_id('submit').first.click()

@when('I send a message to mentor')
def step_impl(context):
    br = context.browser
    br.visit(context.base_url + '/messages/')
    br.fill('message', 'Hello Mentor')
    br.find_by_id('submit').first.click()
