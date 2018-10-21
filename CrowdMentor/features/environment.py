def before_feature(context, feature):
    if feature.name == 'Fixture loading':
        context.fixtures = ['behave-fixtures.json']


def before_scenario(context, scenario):
    if scenario.name == 'Load fixtures for this scenario and feature':
        context.fixtures.append('behave-second-fixture.json')

    if scenario.name == 'Load fixtures then reset sequences':
        context.fixtures.append('behave-second-fixture.json')
        context.reset_sequences = True


def django_ready(context):
    context.django = True

from selenium import webdriver

def before_all(context):
    # PhantomJS is used there (headless browser - meaning we can execute tests in a command-line environment

    context.browser = webdriver.PhantomJS()
    context.browser.implicitly_wait(1)
    context.server_url = 'http://localhost:8000'

def after_all(context):
    # Explicitly quits the browser, otherwise it won't once tests are done
    context.browser.quit()

