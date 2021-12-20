from framework.elements.base.base_element import BaseElement
from framework.utils.logger import Logger


class CheckBox(BaseElement):

    def __init__(self, loc_type, locator, name):
        super(CheckBox, self).__init__(loc_type_of=loc_type, loc=locator, name_of="'{}' checkbox".format(name))

    def check(self, state=True):
        Logger.get_logger().info("Setting value for '{}': {}".format(self.get_name(), state))
        if (state and not self.is_checked()) or (not state and self.is_checked()):
            self.click()

    def uncheck(self):
        self.check(False)

    def is_checked(self):
        return self.find_element().is_selected()

    def is_checked_with_wait(self):
        def func():
            return self.find_element().is_selected()

        return self.wait_for(func)
