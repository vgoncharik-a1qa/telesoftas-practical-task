import pytest

from framework.base_test import BaseTest
from framework.browser.browser import Browser
from framework.utils.config_reader import ConfigReader
from website.pages.challenging_dom_page import ChallengingDomPage
from website.pages.global_sqa_page import GlobalSqaPage


@pytest.mark.web_tests
class TestsTasks(BaseTest):
    def test_second_task(self):
        self.logger.step("Open the 'Challenging DOM' page")
        Browser.set_url(ConfigReader().get_config_by_env()['challenging_dom_url'])
        challenging_dom_page = ChallengingDomPage()
        challenging_dom_page.assert_is_opened()

        self.logger.step("Highlight the cells in the table")
        challenging_dom_page.get_table_form().highlight_cells()

        self.logger.step("Click the 'Green' button")
        challenging_dom_page.click_submit_btn()

    def test_third_task(self):
        self.logger.step("Open the 'Global SQA' page")
        Browser.set_url(ConfigReader().get_config_by_env()['global_sqa_url'])
        global_sqa_page = GlobalSqaPage()
        global_sqa_page.assert_is_opened()

        self.logger.step("Close blue dialog box")
        global_sqa_page.close_blue_dialog_box()

        self.logger.step("Count number of cover images")
        images_count = global_sqa_page.get_count_cover_images()

        self.logger.step("Enter the images number to the search")
        global_sqa_page.fill_in_search(images_count)
