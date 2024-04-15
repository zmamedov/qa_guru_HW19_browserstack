import os

import allure
import pytest
from dotenv import load_dotenv
from appium.options.android import UiAutomator2Options
from selene import browser
from appium import webdriver


@pytest.fixture(scope="session", autouse=True)
def load_env():
    load_dotenv()


@pytest.fixture(scope='function', autouse=True)
def mobile_management():
    login = os.getenv("LOGIN")
    accesskey = os.getenv("ACCESS_KEY")
    options = UiAutomator2Options().load_capabilities({
        "platformName": "android",
        "platformVersion": "9.0",
        "deviceName": "Google Pixel 3",

        "app": "bs://sample.app",

        'bstack:options': {
            "projectName": "First Python project",
            "buildName": "browserstack-build-1",
            "sessionName": "BStack first_test",

            "userName": login,
            "accessKey": accesskey,
        }
    })

    browser.config.driver = webdriver.Remote('http://hub.browserstack.com/wd/hub', options=options)
    browser.config.timeout = float(os.getenv('timeout', '10.0'))

    yield

    # allure.attach(
    #     browser.driver.get_screenshot_as_png(), name='Screenshot', attachment_type=allure.attachment_type.PNG
    # )
    # allure.attach(
    #     browser.driver.page_source, name='XML screen', attachment_type=allure.attachment_type.XML
    # )

    browser.quit()
