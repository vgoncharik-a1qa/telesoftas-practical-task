from framework.elements.base.base_element import BaseElement
from framework.constants import attributes


class Link(BaseElement):

    def __init__(self, loc_type, locator, name):
        super(Link, self).__init__(loc_type_of=loc_type, loc=locator, name_of="'{}' link".format(name))

    def get_href(self):
        return self.get_attribute(attributes.HREF)
