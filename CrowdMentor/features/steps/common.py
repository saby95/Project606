from behave import given, when, then
from test.factories.user import UserFactory

# Home page is not correctly defined!
@then('I am redirected to the home page')
def step_impl(context):
    br = context.browser

    # Checks success status
    print(br.url)
    assert br.url.endswith('/')

@given('I am an existing user who tries to access the site')
def step_impl(context):
    u = UserFactory(username='foo', email='foo@example.com')
    u.set_password('bar')
    # Don't omit to call save() to insert object in database
    u.save()


