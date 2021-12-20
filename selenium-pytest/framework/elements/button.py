from framework.elements.base.base_element import BaseElement


class Button(BaseElement):

    def __init__(self, loc_type, locator, name):
        super(Button, self).__init__(loc_type_of=loc_type, loc=locator, name_of="'{}' button".format(name))

    def is_enabled(self):
        return super(Button, self).is_enabled()
