from selenium.webdriver.common.by import By

from framework.elements.button import Button
from framework.pages.base_page import BasePage
from website.forms.table_form import TableForm


class ChallengingDomPage(BasePage):
    page_locator = "//h3[contains(text(),'Challenging DOM')]"
    btn_submit = Button(By.XPATH, "//a[contains(@class,'button success')]", "Submit")

    def __init__(self):
        super(ChallengingDomPage, self).__init__(loc_type=By.XPATH,
                                                 locator=self.page_locator,
                                                 page_name="Challenging DOM page")

    def get_table_form(self):
        return TableForm()

    def click_submit_btn(self):
        self.btn_submit.click()
