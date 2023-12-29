import time

from selenium.common import NoSuchElementException

from pages.base_page import BasePage


class SQLCodingPage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)
        self.endpoint = self.get_endpoint
        self.checking()

    WORKING_AREA = "//div[contains(@class,'w3-col l')]/div[@class='ws-grey']"
    REQUEST_BLOCK = WORKING_AREA + "//div[contains(@class,'CodeMirror ')]"
    RESULT_BLOCK = WORKING_AREA + "//div[@id='resultSQL']"

    @property
    def get_endpoint(self):
        url = self.get_url()
        return url.split('.com/')[1]

    def checking(self):
        assert self._element.wait_exists(self.REQUEST_BLOCK)\
            and self._element.wait_exists(self.RESULT_BLOCK), "Page was not loaded correctly"
        assert 'sql/trysql.asp' in self.endpoint, "Wrong endpoint"

    def enter_request(self, text: str):
        REQUEST_BLOCK = self.REQUEST_BLOCK + "//div[@class='CodeMirror-code']"

        self._element.clear_request_field(REQUEST_BLOCK)
        self._element.scroll_to(REQUEST_BLOCK)
        try:
            self._element.enter_js_text("#tryitform .CodeMirror", text)
        except:
            self._element.enter_text(REQUEST_BLOCK, text)

    def run_sql(self):
        RUN_BUTTON = self.WORKING_AREA + "//button[@class='ws-btn']"
        self._element.click(RUN_BUTTON)
        time.sleep(1)

    def get_result(self) -> [dict]:
        table_value = self._element.get_iframe_result(self.RESULT_BLOCK + "//iframe")
        return table_value


