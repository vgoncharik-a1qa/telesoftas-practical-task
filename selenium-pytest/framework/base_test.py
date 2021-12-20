import pytest

from framework.browser.browser import Browser
from framework.utils.assertion import Assertion
from framework.utils.logger import Logger
from framework.utils.screenshooter import Screenshooter
from framework.utils.config_reader import ConfigReader


class BaseTest:

    @pytest.fixture(scope='function', autouse=True)
    def test_setup(self):
        self.logger = Logger.get_logger()
        self.assertion = Assertion()
        self.setup_driver()
        yield
        self.destroy_driver()
        self.assertion.assert_all()

    def setup_driver(self):
        """Method implements set up driver and maximize windows."""
        self.logger.test_name(self.__class__.__name__)
        self.logger.info('Starting test...')
        Browser.set_up_driver()
        if not ConfigReader().is_headless():
            Browser.maximize()
        Screenshooter.set_session_screen_dir()

    def destroy_driver(self):
        """Method close browser."""
        Browser.quit()
        self.logger.info('Test Finished\n')
