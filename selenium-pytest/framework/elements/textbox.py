from framework.elements.base.base_element import BaseElement
from framework.utils.logger import Logger


class TextBox(BaseElement):
    def __init__(self, loc_type, locator, name):
        super(TextBox, self).__init__(loc_type_of=loc_type, loc=locator, name_of="'{}' textbox".format(name))

    def type(self, text):
        Logger.get_logger().info("Type text to {}: {}".format(self.get_name(), text))
        self.send_keys(text)

    def clear(self):
        self.find_element().clear()

    def clear_and_type(self, text):
        self.clear()
        self.type(text)
