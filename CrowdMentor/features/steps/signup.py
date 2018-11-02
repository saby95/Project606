from behave import given, when, then
from test.factories.user import UserFactory

@given('a new user tries to access the site')
def step_impl(context):
    u = UserFactory(username='foo', email='foo@example.com')
    u.set_password('bar')

    # Don't omit to call save() to insert object in database
    u.save()

@when('I submit a valid signup page')
def step_impl(context):
    br = context.browser
    br.visit(context.base_url + '/signup/')

    # Fill login form and submit it (valid version)
    br.fill('username', 'foo')
    br.fill('first_name', 'foo')
    br.fill('last_name', 'bar')
    br.fill('email', 'email@example.com')
    br.fill('password1', 'Abcd@1234')
    br.fill('password2', 'Abcd@1234')
    br.fill('birth_date', '04/12/1996')
    br.find_by_id('id_signup').first.click()

@when('I submit an invalid signup page')
def step_impl(context):
    br = context.browser

    br.visit(context.base_url + '/signup/')

    # Fill login form and submit it (invalid version)
    br.fill('username', 'foo')
    br.fill('first_name', 'foo')
    br.fill('last_name', 'bar')
    br.fill('email', 'email@example.com')
    br.fill('password1', 'Abcd@1234')
    br.fill('password2', 'Abcd@1234')
    br.fill('birth_date', '04/12/1996')
    br.find_by_id('id_signup').first.click()

@then('I get an error message saying that a user with that username already exists.')
def step_impl(context):
    br = context.browser

    # Checks redirection URL
    assert br.url.endswith('/signup/')
    assert br.find_by_id('error').text == "A user with that username already exists."
