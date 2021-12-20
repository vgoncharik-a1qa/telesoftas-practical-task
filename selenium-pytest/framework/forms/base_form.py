from framework.elements.label import Label
from framework.utils.screenshooter import Screenshooter


class BaseForm:
    def __init__(self, loc_type, locator, form_name):
        self.locator = locator
        self.form_name = form_name
        self.loc_type = loc_type

    def is_opened(self):
        return Label(self.loc_type, self.locator, self.form_name).is_visible_with_wait()

    def wait_for_form_closed(self):
        Label(self.loc_type, self.locator, self.form_name).wait_for_is_absent()

    def wait_for_form_opened(self):
        Label(self.loc_type, self.locator, self.form_name).wait_for_is_visible()

    def assert_is_opened(self):
        if not self.is_opened():
            Screenshooter.take_screenshot()
            assert False, "'{}' is NOT opened".format(self.form_name)
