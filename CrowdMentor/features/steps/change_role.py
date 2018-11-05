from behave import given, when, then
from test.factories.user import UserFactory

@when('I change any user role')
def step_impl(context):
    br = context.browser
    br.visit(context.base_url + '/change_roles/')

    # Fill login form and submit it (valid version)
    br.find_by_id('id_role_2').first.select('mentor')
    br.find_by_id('id_change_role').first.click()
