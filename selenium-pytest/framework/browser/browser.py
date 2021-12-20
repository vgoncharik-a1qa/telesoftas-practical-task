from selenium.common.exceptions import NoSuchWindowException, TimeoutException, NoAlertPresentException
from selenium.webdriver.support.wait import WebDriverWait

from configuration import config
from framework.browser.browser_factory import BrowserFactory
from framework.utils.logger import Logger
from framework.waits.waits import WaitForReadyStateComplete, WaitForTrue
from framework.utils.config_reader import ConfigReader
from framework.scripts import scripts_js


class Browser:
    __web_driver = None
    __main_window_handle = None

    @staticmethod
    def get_driver():
        return Browser.__web_driver

    @staticmethod
    def set_up_driver():
        Logger.get_logger().info("Browser initialisation for '{}'".format(ConfigReader().get_browser().capitalize()))
        Browser.__web_driver = BrowserFactory.get_browser_driver()
        Logger.get_logger().info("{} version: {}".format(ConfigReader().get_browser().capitalize(), Browser.version()))
        Browser.__web_driver.implicitly_wait(config.IMPLICITLY_WAIT_SEC)
        Browser.__web_driver.set_page_load_timeout(config.PAGE_LOAD_TIMEOUT_SEC)
        Browser.__web_driver.set_script_timeout(config.SCRIPT_TIMEOUT_SEC)
        Browser.__main_window_handle = Browser.__web_driver.current_window_handle

    @staticmethod
    def quit():
        if Browser.get_driver() is not None:
            Logger.get_logger().info("Destroy driver")
            Browser.get_driver().quit()
            Browser.__web_driver = None

    @staticmethod
    def close(page_name=""):
        if Browser.get_driver() is not None:
            Logger.get_logger().info("Page %s closing " % page_name)
            Browser.get_driver().close()

    @staticmethod
    def refresh_page():
        Logger.get_logger().info("Page refresh")
        Browser.get_driver().refresh()

    @staticmethod
    def maximize():
        Browser.get_driver().maximize_window()

    @staticmethod
    def set_url(url):
        Logger.get_logger().info("Change page url to: " + url)
        Browser.get_driver().get(url)

    @staticmethod
    def set_host_url(endpoint=None):
        url = ConfigReader().get_host_url()
        if endpoint:
            url = url + endpoint
        Browser.set_url(url)

    @staticmethod
    def execute_script(script, *args):
        return Browser.get_driver().execute_script(script, *args)

    @staticmethod
    def get_current_url():
        return Browser.get_driver().current_url

    @staticmethod
    def back_page():
        Browser.get_driver().back()

    @staticmethod
    def switch_to_window(window_handle):
        Logger.get_logger().info("Switch to window with name %s" % window_handle)
        try:
            Browser.get_driver().switch_to.window(window_handle)
        except NoSuchWindowException:
            Logger.get_logger().error("No matching window %s found" % window_handle)

    @staticmethod
    def switch_main_window():
        Logger.get_logger().info("Switch to main window")
        try:
            Browser.get_driver().switch_to.window(Browser.__main_window_handle)
        except NoSuchWindowException:
            Logger.get_logger().error("Main window not found")

    @staticmethod
    def switch_new_window(page_name=""):
        Logger.get_logger().info("Switch to new window %s" % page_name)
        handles = Browser.get_driver().window_handles
        if len(handles) <= 1:
            raise NoSuchWindowException("New window is absent. Windows amount = %s" % len(handles))
        Browser.get_driver().switch_to.window(handles[-1])

    @staticmethod
    def switch_to_frame(frame_name):
        Logger.get_logger().info("Switch to frame with name '%s'" % frame_name)
        Browser.get_driver().switch_to.frame(frame_name)

    @staticmethod
    def get_alert():
        Logger.get_logger().info("Get alert")
        try:
            return Browser.get_driver().switch_to.alert()
        except NoAlertPresentException:
            Logger.get_logger().info("Alert window not found")
            return None

    @staticmethod
    def accept_alert_if_exist():
        Logger.get_logger().info("Accept alert if exist")
        alert = Browser.get_alert()
        if alert is not None:
            alert.accept()
            Logger.get_logger().info("Alert accepted")

    @staticmethod
    def get_alert_text():
        Logger.get_logger().info("Get alert text")
        alert = Browser.wait_for_true(Browser.get_alert)
        return alert.text

    @staticmethod
    def switch_to_default_content():
        Logger.get_logger().info("Switch to default frame")
        Browser.get_driver().switch_to.default_content()

    @staticmethod
    def scroll_to_top():
        Logger.get_logger().info("Scroll to top")
        Browser.execute_script(scripts_js.SCROLL_TO_TOP)

    @staticmethod
    def scroll_to_bottom():
        Logger.get_logger().info("Scroll to bottom")
        Browser.execute_script(scripts_js.SCROLL_TO_BOTTOM)

    @staticmethod
    def wait_for_page_to_load():
        WebDriverWait(Browser.get_driver(), config.PAGE_LOAD_TIMEOUT_SEC).until(WaitForReadyStateComplete(Browser))

    @staticmethod
    def turn_off_implicit_wait():
        Browser.__web_driver.implicitly_wait(0)

    @staticmethod
    def set_implicit_wait(wait_time_sec=config.IMPLICITLY_WAIT_SEC):
        Browser.__web_driver.implicitly_wait(wait_time_sec)

    @staticmethod
    def wait_for_true(expression, time_in_seconds=config.IMPLICITLY_WAIT_SEC, msg=""):
        try:
            return WebDriverWait(Browser.get_driver(), time_in_seconds).until(WaitForTrue(Browser, expression))
        except TimeoutException:
            error_msg = "During {time} seconds action was not made: {msg}".format(time=time_in_seconds,
                                                                                  msg=msg)
            Logger.get_logger().error(error_msg)
            raise TimeoutException(error_msg)

    @staticmethod
    def version():
        return Browser.__web_driver.capabilities['browserVersion']
