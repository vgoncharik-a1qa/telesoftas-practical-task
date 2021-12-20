from selenium.webdriver.support.ui import Select
from framework.elements.base.base_element import BaseElement
from framework.browser.browser import Browser
from framework.utils.logger import Logger
from framework.scripts import scripts_js


class ComboBox(BaseElement):

    def __init__(self, loc_type, locator, name):
        super(ComboBox, self).__init__(loc_type_of=loc_type, loc=locator, name_of="'{}' combobox".format(name))

    def select_by_text(self, text):
        Logger.get_logger().info("Select in the {}: {}".format(self.get_name(), text))

        def func():
            Select(self.find_element()).select_by_visible_text(text)
            return True
        self.wait_for(func)

    def select_by_index(self, index):
        Logger.get_logger().info("Select in the {}: {}".format(self.get_name(), index))

        def func():
            Select(self.find_element()).select_by_index(index)
            return True
        self.wait_for(func)

    def select_by_value(self, value):
        Logger.get_logger().info("Select in the {}: {}".format(self.get_name(), value))

        def func():
            Select(self.find_element()).select_by_value(value)
            return True
        self.wait_for(func)

    def get_selected_options(self):
        def func():
            return Select(self.find_element()).all_selected_options
        self.wait_for(func)

    def get_options(self):
        def func():
            return Select(self.find_element()).options
        self.wait_for(func)

    def select2_by_text_via_js(self, text):
        Logger.get_logger().info("Select in the {}: {}".format(self.get_name(), text))
        self.wait_for_is_present()
        Browser.execute_script(scripts_js.SELECT2_SELECT_BY_TEXT, self.find_element(), text)

    def select2_by_value_via_js(self, value):
        Logger.get_logger().info("Select in the {}: {}".format(self.get_name(), value))
        self.wait_for_is_present()
        Browser.execute_script(scripts_js.SELECT2_SELECT_BY_VALUE, self.find_element(), value)

    def get_selected2_options_via_js(self):
        self.wait_for_is_present()
        return Browser.execute_script(scripts_js.SELECT2_GET_SELECTED_OPTIONS, self.find_element())
