from behave import given, when, then
from test.factories.user import UserFactory


@given('an admin logged in')
def step_impl(context):
    from django.contrib.auth.models import User

    # Creates a dummy user for our tests (user is not authenticated at this point)
    u = UserFactory(username='admin', email='admin@example.com')
    u.set_password('bar@1231')

    # Don't omit to call save() to insert object in database
    u.save()

    u1 = UserFactory(username='foo', email='foo@example.com')
    u1.set_password('bar')

    # Don't omit to call save() to insert object in database
    u1.save()

    client = context.test.client
    res = client.login(usename='admin', password='bar@1231')

    cookie = client.cookies['sessionId']

    # Selenium will set cookie domain based on current page domain.
    context.browser.get(context.get_url('/change_roles/'))
    context.browser.add_cookie({
        'name': 'sessionid',
        'value': cookie.value,
        'secure': False,
        'path': '/',
    })


@when('I change any user role')
def step_impl(context):
    br = context.browser
    br.visit(context.base_url + '/change_roles/')

    # Fill login form and submit it (valid version)
    #br.find_element_by_id('role_2').send_keys('foo')
    br.find_by_id('id_change_role').first.click()
