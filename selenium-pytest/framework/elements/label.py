from framework.elements.base.base_element import BaseElement


class Label(BaseElement):

    def __init__(self, loc_type, locator, name):
        super(Label, self).__init__(loc_type_of=loc_type, loc=locator, name_of="'{}' label".format(name))
