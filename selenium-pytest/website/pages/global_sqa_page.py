from selenium.webdriver.common.by import By

from framework.elements.button import Button
from framework.elements.label import Label
from framework.elements.textbox import TextBox
from framework.pages.base_page import BasePage
from framework.browser.browser import Browser


class GlobalSqaPage(BasePage):
    page_locator = "//img[@alt='GlobalSQA']"
    iframe_name = "globalSqa"
    btn_close_dialog_box = Button(By.XPATH, "//div[@rel-title='iFrame']//a[contains(@class,'close_img')]", "Close dialog box")
    lbl_cover_image = Label(By.XPATH, "//div[@id='portfolio_items']//img[contains(@class,'wp-post-image')]", "Cover image")
    search_loc = "//body[contains(@class,'page_sidebar')]//form[@class='search']"
    tbx_search = TextBox(By.XPATH, search_loc + "/input", "Search")
    btn_search = Button(By.XPATH, search_loc + "/button", "Search")

    def __init__(self):
        super(GlobalSqaPage, self).__init__(loc_type=By.XPATH,
                                            locator=self.page_locator,
                                            page_name="Global SQA page")

    def close_blue_dialog_box(self):
        self.btn_close_dialog_box.click()

    def get_count_cover_images(self):
        Browser.switch_to_frame(self.iframe_name)
        count = self.lbl_cover_image.get_elements_count()
        Browser.switch_to_default_content()
        return count

    def fill_in_search(self, text):
        Browser.scroll_to_top()
        self.tbx_search.type(text)
        self.btn_search.click()
