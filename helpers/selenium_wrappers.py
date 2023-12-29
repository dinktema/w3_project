from selenium.common import TimeoutException, NoSuchElementException, WebDriverException, InvalidSelectorException
from selenium import webdriver
from selenium.webdriver import ActionChains, Keys
from selenium.webdriver.common import action_chains
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from bs4 import BeautifulSoup


class Element:
    def __init__(self, driver, timeout=False):
        self._driver = driver
        self._timeout = timeout
        self._wait = WebDriverWait(self._driver, timeout=self._timeout)
        self.actions = ActionChains(self._driver)

    def _get(self, locator: str) -> WebElement:
        try:
            return self._wait.until(ec.presence_of_element_located((By.XPATH, locator)))
        except TimeoutException:
            raise Exception(f"Element was not found on page.\nLocator: '{locator}'")

    def scroll_to(self, locator: str):
        target = self._get(locator)
        self._driver.execute_script('arguments[0].scrollIntoView(false);', target)

    def enter_js_text(self, input_attr: str, text: str):
        self._driver.execute_script(f"document.querySelector('{input_attr}').CodeMirror.setValue((r'{text}'))")

    def enter_text(self, locator: str,  text: str):
        element = self._get(locator)
        self.actions.click(element).perform()
        self.actions.send_keys(text).perform()

    def clear_request_field(self, locator: str):
        element = self._get(locator)
        if value := self.get_js_value('#textareaCodeSQL'):
            self.actions.click(element).perform()
            for i in range(len(value)):
                self.actions.send_keys(Keys.BACKSPACE).perform()

    def get_js_value(self, js_attr: str):
        value = self._driver.execute_script(f"return document.querySelector('{js_attr}').value")
        return value

    def click(self, locator: str):
        try:
            self._get(locator).click()
            return True
        except TimeoutException:
            raise Exception(f"Element is not clickable.\nLocator: {locator}")

    def wait_exists(self, locator: str) -> bool:
        try:
            return self._wait.until(lambda x: x.find_element(By.XPATH, locator))
        except TimeoutException:
            return False

    def get_iframe_result(self, locator: str) -> [dict]:
        def table_scrapping():
            frame = self._get("//body").get_attribute('outerHTML')
            soup = BeautifulSoup(frame, 'html.parser')
            rows = soup.find_all('tr')
            data = []
            if rows:
                columns = [cell.text.strip() for cell in rows[0].find_all('th')]
                for row in rows[1:]:
                    values = [cell.text.strip() for cell in row.find_all('td')]
                    record = dict(zip(columns, values))
                    data.append(record)
                return data
            else:
                return self._get("//body").text.replace("\'", '')

        try:
            self._driver.switch_to.frame(frame_reference=self._get(locator))
            return table_scrapping()
        except Exception as e:
            raise Exception(e)
        finally:
            self._driver.switch_to.default_content()
