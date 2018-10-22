from behave import given, when, then
from test.factories.user import UserFactory

@given('a new user tries to access the site')
def step_impl(context):
    u = UserFactory(username='foo1', email='foo@example.com')
    u.set_password('bar')

    # Don't omit to call save() to insert object in database
    u.save()

@when('I submit a valid signup page')
def step_impl(context):
    br = context.browser
    br.get(context.base_url + '/signup/')

    # Fill login form and submit it (valid version)
    br.find_element_by_id('id_username').send_keys('foo')
    br.find_element_by_id('id_first_name').send_keys('bar')
    br.find_element_by_id('id_last_name').send_keys('foo')
    br.find_element_by_id('id_email').send_keys('bar@gmail.com')
    br.find_element_by_id('id_password1').send_keys('Abcd@1234')
    br.find_element_by_id('id_password2').send_keys('Abcd@1234')
    br.find_element_by_id('id_birth_date').send_keys('02/02/1995')
    br.find_element_by_id('id_signup').click()

@when('I submit an invalid signup page')
def step_impl(context):
    br = context.browser

    br.get(context.base_url + '/signup/')

    # Fill login form and submit it (invalid version)

    br.find_element_by_id('id_username').send_keys('foo1')
    br.find_element_by_id('id_first_name').send_keys('bar1')
    br.find_element_by_id('id_last_name').send_keys('foo1')
    br.find_element_by_id('id_email').send_keys('bar1@gmail.com')
    br.find_element_by_id('id_password1').send_keys('Abcd@1234')
    br.find_element_by_id('id_password2').send_keys('Abcd@1234')
    br.find_element_by_id('id_birth_date').send_keys('02/02/1995')
    br.find_element_by_id('id_signup').click()


@then('I get an error message saying that a user with that username already exists.')
def step_impl(context):
    br = context.browser

    # Checks redirection URL
    assert br.current_url.endswith('/signup/')
    assert br.find_element_by_id('error').text == "A user with that username already exists."