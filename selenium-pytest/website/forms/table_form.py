from selenium.webdriver.common.by import By

from framework.forms.base_form import BaseForm
from framework.elements.label import Label
from framework.elements.link import Link


class TableForm(BaseForm):
    form_locator = "//div[contains(@class,'large-10')]/table"
    cell_by_indexes_loc = "table tbody tr:nth-of-type({}) td:nth-of-type({})"
    cell_by_row_index_and_column_name_loc = "//tbody/tr[{}]/td[count(//thead//th[text()='{}']/preceding-sibling::th)+1]"
    row_by_cell_value_loc = "//tbody//tr[count(//tbody//td[text()='{}']/parent::tr/preceding-sibling::tr)+1]"
    delete_lnk_by_value_in_row_loc = row_by_cell_value_loc + "//a[contains(@href,'delete')]"
    edit_lnk_by_value_in_row_loc = row_by_cell_value_loc + "//a[contains(@href,'edit')]"
    cell_by_value_loc = "//tbody//td[contains(text(),'{}')]"

    def __init__(self):
        super(TableForm, self).__init__(loc_type=By.XPATH, locator=self.form_locator, form_name="Table")

    def get_cell_by_indexes(self, row_index, column_index):
        return Label(By.CSS_SELECTOR, self.cell_by_indexes_loc.format(row_index, column_index), "Cell")

    def get_cell_by_row_index_and_column_name(self, row_index, column_name):
        return Label(By.XPATH, self.cell_by_row_index_and_column_name_loc.format(row_index, column_name), "Cell")

    def get_delete_link_by_value_in_row(self, cell_value):
        return Link(By.XPATH, self.delete_lnk_by_value_in_row_loc.format(cell_value), "Delete")

    def get_edit_link_by_value_in_row(self, cell_value):
        return Link(By.XPATH, self.edit_lnk_by_value_in_row_loc.format(cell_value), "Edit")

    def get_cell_by_value(self, cell_value):
        return Label(By.XPATH, self.cell_by_value_loc.format(cell_value), "Cell")

    def highlight_cells(self):
        self.get_cell_by_row_index_and_column_name(3, 'Diceret').highlight_with_pause()
        self.get_delete_link_by_value_in_row('Apeirian7').highlight_with_pause()
        self.get_edit_link_by_value_in_row('Apeirian2').highlight_with_pause()
        self.get_cell_by_value('Definiebas7').highlight_with_pause()
        self.get_cell_by_value('Iuvaret7').highlight_with_pause()
