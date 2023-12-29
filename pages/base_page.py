from helpers.selenium_wrappers import Element


class BasePage:
    """Common properties and attributes"""
    def __init__(self, driver):
        self._driver = driver
        self._element = Element(driver)

    def get_url(self):
        return self._driver.current_url

