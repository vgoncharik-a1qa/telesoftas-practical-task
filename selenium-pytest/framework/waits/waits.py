from selenium.common.exceptions import StaleElementReferenceException
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.wait import WebDriverWait

from framework.scripts import scripts_js


class WaitForReadyStateComplete(object):
    STATE_COMPLETE = "complete"

    def __init__(self, browser):
        self.browser = browser

    def __call__(self, driver):
        try:
            return self.browser.execute_script(scripts_js.GET_PAGE_READY_STATE) == WaitForReadyStateComplete.STATE_COMPLETE
        except StaleElementReferenceException:
            return False


class WaitForTrue(object):
    def __init__(self, browser, expression):
        self.browser = browser
        self.expression = expression

    def __call__(self, driver):
        try:
            return self.expression()
        except Exception:
            return False


class WaitForCondition(object):
    def __init__(self, condition):
        self.condition = condition

    def __call__(self, driver):
        try:
            return self.condition()
        except Exception:
            return False


def wait_for_condition(condition, timeout):
    try:
        WebDriverWait(None, timeout).until(WaitForCondition(condition))
        return True
    except TimeoutException:
        return False
