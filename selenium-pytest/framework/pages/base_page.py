from framework.browser.browser import Browser
from framework.elements.label import Label
from framework.utils.screenshooter import Screenshooter


class BasePage:
    def __init__(self, loc_type, locator, page_name):
        self.locator = locator
        self.page_name = page_name
        self.loc_type = loc_type

    def wait_page_to_load(self):
        Browser.wait_for_page_to_load()

    def is_opened(self):
        self.wait_page_to_load()
        return Label(self.loc_type, self.locator, self.page_name).is_visible_with_wait()

    def wait_for_page_closed(self):
        self.wait_page_to_load()
        Label(self.loc_type, self.locator, self.page_name).wait_for_is_absent()

    def wait_for_page_opened(self):
        self.wait_page_to_load()
        Label(self.loc_type, self.locator, self.page_name).wait_for_is_visible()

    def refresh_page(self):
        Browser.refresh_page()

    def assert_is_opened(self):
        if not self.is_opened():
            Screenshooter.take_screenshot()
            assert False, "'{}' is NOT opened".format(self.page_name)
