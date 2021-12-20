import random
from selenium.common.exceptions import TimeoutException, StaleElementReferenceException
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from configuration import config
from configuration.config import EXPLICITLY_WAIT_SEC, IS_EXIST_WAIT_SEC
from framework.browser.browser import Browser
from framework.scripts import scripts_js
from framework.constants import attributes
from framework.utils.logger import Logger


class BaseElement(object):
    coordinate_x = 'x'
    coordinate_y = 'y'

    def __init__(self, loc_type_of, loc, name_of):
        self.__loc_type = loc_type_of
        self.__locator = loc
        self.__name = name_of

    def __getitem__(self, key):
        if (self.__loc_type != By.XPATH):
            raise TypeError("__getitem__ for BaseElement possible only when __loc_type == By.XPATH")
        else:
            return BaseElement(By.XPATH, self.__locator + "[" + str(key) + "]", self.__name)

    def get_locator(self):
        return self.__locator

    def get_loc_type(self):
        return self.__loc_type

    def get_name(self):
        return self.__name

    def find_element(self):
        element = self.wait_for_check_by_condition(method_to_check=EC.presence_of_element_located,
                                                   message=" was not found")
        return element

    @staticmethod
    def get_displayed_elements(condition, locator):
        element_size = len(Browser.get_driver().find_elements(condition, locator))
        result_elements = []
        try:
            for ele_number in range(1, element_size + 1):
                element_locator = "({locator})[{number}]".format(locator=locator, number=ele_number)
                Logger.get_logger().info("Element searching with locator " + element_locator)
                element = WebDriverWait(Browser.get_driver(), EXPLICITLY_WAIT_SEC).until(
                    EC.visibility_of_element_located((condition, element_locator)))
                result_elements.append(element)
        except TimeoutException:
            error_msg = "element with locator was not found"
            Logger.get_logger().error(error_msg)
            raise TimeoutException(error_msg)
        return result_elements

    def is_enabled(self):
        def func():
            return self.find_element().is_enabled()
        return self.wait_for(func)

    def is_disabled(self):
        return not self.is_enabled()

    def is_displayed(self):
        def func():
            return self.find_element().is_displayed()
        return self.wait_for(func)

    def is_present(self):
        return self.get_elements_count() > 0

    def get_elements_count(self):
        elements_count = len(self.get_elements())
        return elements_count

    def get_elements(self):
        def func():
            return Browser.get_driver().find_elements(self.__loc_type, self.__locator)
        Browser.wait_for_page_to_load()
        Browser.set_implicit_wait(config.IS_PRESENT_IMPLICITLY_WAIT_SEC)
        elements = self.wait_for(func)
        Browser.set_implicit_wait()
        return elements

    def get_rnd_element(self):
        elements = self.get_elements()
        element = elements[random.randint(0, len(elements) - 1)]
        return element

    def get_elements_text(self):
        return [elem.text for elem in self.get_elements()]

    def get_elements_attribute(self, attribute):
        return [elem.get_attribute(name=attribute) for elem in self.get_elements()]

    def get_element_contains_text(self, text):
        for elem in self.get_elements():
            if text in elem.text:
                return elem

    def get_displayed_element(self):
        elements = self.get_elements()
        for element in elements:
            if element.is_displayed():
                return element

    def send_keys(self, key):
        def func(key):
            self.find_element().send_keys(key)
            return True
        self.wait_for(func, key)

    def click(self):
        Logger.get_logger().info("Click the " + self.get_name())

        def func():
            self.wait_for_check_by_condition(method_to_check=EC.element_to_be_clickable,
                                             message=" doesn't exist or clickable")
            self.find_element().click()
            return True
        self.wait_for(func)

    def click_via_js(self):
        Logger.get_logger().info("Click the " + self.get_name())
        return Browser.execute_script(scripts_js.CLICK_ELEMENT, self.find_element())

    def get_text(self):
        def func():
            return self.find_element().text
        return self.wait_for(func)

    def get_value(self):
        def func():
            return self.get_attribute(attributes.VALUE)
        return self.wait_for(func)

    def get_text_content_via_js(self):
        def func():
            return Browser.execute_script(scripts_js.GET_TEXT_CONTENT_FOR_ELEMENT, self.find_element())
        return self.wait_for(func)

    def get_attribute(self, attr):
        Logger.get_logger().info("Get '{}' attribute for {}".format(attr, self.get_name()))

        def func(attr):
            return self.find_element().get_attribute(name=attr)
        return self.wait_for(func, attr)

    def set_attribute_via_js(self, attr, value):
        if value:
            Logger.get_logger().info("Set '{}' attribute for {} to: {}".format(attr, self.get_name(), value))
        Browser.execute_script(scripts_js.SET_ATTRIBUTE_TO_ELEMENT, self.find_element(), attr, value)

    def set_text_via_js(self, text):
        Logger.get_logger().info("Set '{}' text to: {}".format(text, self.get_name()))
        Browser.execute_script(scripts_js.SET_TEXT_TO_ELEMENT, self.find_element(), text)

    def scroll_via_js(self, is_top=True):
        self.wait_for_is_visible()
        Logger.get_logger().info("Scroll to " + self.get_name())
        Browser.execute_script(scripts_js.SCROLL_INTO_VIEW, self.find_element(), is_top)

    def double_click(self):
        self.wait_for_is_visible()
        Logger.get_logger().info("Double click by " + self.get_name())

        def func():
            ActionChains(Browser.get_driver()).double_click(self.find_element()).perform()
        self.wait_for(func)

    def move_to_element(self):
        self.wait_for_is_visible()
        Logger.get_logger().info("Move to " + self.get_name())
        ActionChains(Browser.get_driver()).move_to_element(self.find_element()).perform()

    def focus(self):
        self.wait_for_is_visible()
        Browser.execute_script(scripts_js.SET_FOCUS, self.find_element())

    def highlight(self):
        self.wait_for_is_visible()
        Browser.execute_script(scripts_js.BORDER_ELEMENT, self.find_element())

    def highlight_with_pause(self, duration=2):
        self.wait_for_is_visible()
        Logger.get_logger().info("Highlight the {} and pause for: {}".format(self.get_name(), duration))
        self.highlight()
        ActionChains(Browser.get_driver()).pause(duration).perform()
        self.set_attribute_via_js(attributes.STYLE, '')

    def is_visible_with_wait(self):
        try:
            self.wait_for_is_visible()
        except TimeoutException:
            return False
        return True

    def is_absent_with_wait(self):
        try:
            self.wait_for_is_absent()
        except TimeoutException:
            return False
        return True

    def wait_for_is_visible(self):
        self.wait_for_check_by_condition(method_to_check=EC.visibility_of_element_located,
                                         message=" doesn't exist")

    def wait_for_is_present(self):
        self.wait_for_check_by_condition(method_to_check=EC.presence_of_element_located,
                                         message=" doesn't exist")

    def wait_for_is_displayed(self):
        Browser.wait_for_true(self.is_displayed)

    def wait_for_is_absent(self):
        Browser.turn_off_implicit_wait()
        self.wait_for_check_by_condition(method_to_check=EC.invisibility_of_element_located,
                                         message=" already exists", wait_time_sec=IS_EXIST_WAIT_SEC)
        Browser.set_implicit_wait()

    def wait_for_element_disappear(self):
        def func():
            return len(self.find_element()) == 0
        self.wait_for(func)

    def wait_for_text(self, text):
        def func(text):
            return text in self.get_text()
        self.wait_for(func, text)

    def wait_for_value(self, text):
        def func(text):
            return text in self.get_value()
        self.wait_for(func, text)

    def wait_for_check_by_condition(self, method_to_check, message, wait_time_sec=EXPLICITLY_WAIT_SEC,
                                    use_default_msg=True):
        try:
            element = WebDriverWait(Browser.get_driver(),
                                    wait_time_sec,
                                    ignored_exceptions=[StaleElementReferenceException]).\
                until(method=method_to_check((self.get_loc_type(), self.get_locator())))
        except TimeoutException:
            result_message = (self.get_name() + " with locator " + self.get_locator() + message
                              if use_default_msg else message)
            Logger.get_logger().warning(result_message)
            raise TimeoutException(result_message)
        return element

    def get_location(self):
        def func():
            return self.find_element().location
        return self.wait_for(func)

    def get_location_vertical(self):
        def func():
            return self.find_element().location[BaseElement.coordinate_y]
        return self.wait_for(func)

    def get_location_horizontal(self):
        def func():
            return self.find_element().location[BaseElement.coordinate_x]
        return self.wait_for(func)

    @staticmethod
    def get_list_of_elements_vertical_locations(condition, locator):
        other_elements = BaseElement.get_displayed_elements(condition, locator)
        return [element.location[BaseElement.coordinate_y] for element in other_elements]

    @staticmethod
    def get_dict_of_elements_vertical_locations_and_text(condition, locator):
        events_time_elements = BaseElement.get_displayed_elements(condition, locator)
        events_info = {}
        for element in events_time_elements:
            events_info[element.location[BaseElement.coordinate_y]] = element.text
        return events_info

    def wait_for(self, condition, *args, **kwargs):
        def func(driver):
            try:
                value = condition(*args, **kwargs)
                return value
            except StaleElementReferenceException:
                return False
        return WebDriverWait(Browser.get_driver(),
                             EXPLICITLY_WAIT_SEC,
                             ignored_exceptions=[StaleElementReferenceException]).until(func)
