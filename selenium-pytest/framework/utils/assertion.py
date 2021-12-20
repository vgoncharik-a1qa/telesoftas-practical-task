from hamcrest import *
from hamcrest.core.matcher import Matcher
from hamcrest.core.string_description import StringDescription

from framework.utils.logger import Logger
from framework.utils.screenshooter import Screenshooter


class Assertion(object):
    def __init__(self):
        self.verification_errors = []

    def should_be_true(self, condition, msg=None):
        self._assertion(condition, equal_to(True), reason=msg)

    def should_be_equal(self, actual, expected, msg=None):
        self._assertion(actual, equal_to(expected), reason=msg)

    def should_be_equal_to_table(self, actual, expected, msg=None):
        for row in zip(actual, expected):
            self.should_be_equal(row[0], row[1], msg)

    def should_contain_dict(self, container, items, msg=None):
        for key, value in items.items():
            self._assertion(
                container.get(key), contains_string(value), reason=f'{msg}: {key} (key {"present" if key in container else "absent"})')

    def should_contain_dict_in_list_of_dict(self, containers, items, msg=None):
        for container in containers:
            self.should_contain_dict(container, items, msg)

    def should_contain_table(self, actual, expected, msg=None):
        for row in zip(actual, expected):
            self.should_contain_dict(row[0], row[1], msg)

    def should_contain_string(self, container, item, msg=None):
        self._assertion(container, contains_string(item), reason=msg)

    def should_contain_string_in_list(self, items, string, msg=None):
        for item in items:
            self.should_contain_string(item.lower(), string.lower(), msg)

    def should_matches_regexp(self, string, regexp, msg=None):
        self._assertion(string, matches_regexp(regexp), reason=msg)

    def assert_all(self):
        msg = 'The following {} assert(s) failed:\n\n'.format(len(self.verification_errors))
        for error in self.verification_errors:
            msg = msg + error + "\n"
        if not self.verification_errors == []:
            self.verification_errors = []
            raise AssertionError(msg)

    def _assertion(self, actual, matcher=None, reason="Assertion failed"):
        if isinstance(matcher, Matcher):
            if not matcher.matches(actual):
                description = StringDescription()
                description.append_text(reason)\
                    .append_text(":\n   Expected: ")\
                    .append_description_of(matcher)\
                    .append_text("\n        but: ")
                matcher.describe_mismatch(actual, description)
                self._collect_errors(description)
        else:
            if isinstance(actual, Matcher):
                Logger.get_logger().warning("arg1 should be boolean, but was {}".format(type(actual)))
            self._collect_errors(reason)

    def _collect_errors(self, msg):
        Logger.get_logger().error(msg)
        Screenshooter.take_screenshot()
        counter = len(self.verification_errors) + 1
        self.verification_errors.append('{}. {}\n'.format(counter, msg))
