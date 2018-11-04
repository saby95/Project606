from behave import given, when, then
from test.factories.user import UserFactory

@when('I submit a valid login page')
def step_impl(context):
    br = context.browser
    br.visit(context.base_url + '/login/')

    # Fill login form and submit it (valid version)
    br.fill('username', 'foo')
    br.fill('password', 'bar')
    br.find_by_id('submit').first.click()

@when('I submit an invalid login page')
def step_impl(context):
    br = context.browser

    br.visit(context.base_url + '/login/')

    # Fill login form and submit it (invalid version)
    br.fill('username', 'foo')
    br.fill('password', 'bar-is-invalid')
    br.find_by_id('submit').first.click()

@then('I get an error message saying that my username and password did not match.')
def step_impl(context):
    br = context.browser

    # Checks redirection URL
    assert br.url.endswith('/login/')
    assert br.find_by_id('error').text == "Your username and password didn't match. Please try again."
