from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager

from framework.constants import browsers
from framework.utils.config_reader import ConfigReader


class BrowserFactory:

    @staticmethod
    def get_browser_driver():
        browser = ConfigReader().get_browser()
        remote = ConfigReader().is_remote()
        headless = ConfigReader().is_headless()
        if browser == browsers.BROWSER_CHROME:
            return BrowserFactory.get_chrome_driver(headless, remote)
        elif browser == browsers.BROWSER_FIREFOX:
            return BrowserFactory.get_firefox_driver(headless, remote)
        else:
            raise ValueError("Unknown browser '{}'".format(browser))

    @staticmethod
    def get_chrome_driver(headless, remote):
        chrome_options = ChromeOptions()
        chrome_options.add_argument('--ignore-certificate-errors')
        if headless:
            chrome_options.add_argument('--headless')
            chrome_options.add_argument('--window-size=1920x1080')
        if remote:
            return BrowserFactory.get_remote_driver(chrome_options.to_capabilities())
        else:
            return webdriver.Chrome(executable_path=ChromeDriverManager().install(), options=chrome_options)

    @staticmethod
    def get_firefox_driver(headless, remote):
        firefox_options = FirefoxOptions()
        if headless:
            firefox_options.headless = True
            firefox_options.add_argument("--width=1920")
            firefox_options.add_argument("--height=1080")
        if remote:
            return BrowserFactory.get_remote_driver(firefox_options.to_capabilities())
        else:
            return webdriver.Firefox(executable_path=GeckoDriverManager().install(), options=firefox_options)

    @staticmethod
    def get_remote_driver(capabilities):
        return webdriver.Remote(ConfigReader().get_remote_url(), desired_capabilities=capabilities)
