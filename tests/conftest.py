import os

import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

server = 'https://www.w3schools.com'


@pytest.fixture(scope='module')
def setup(request):
    opt = Options()
    if os.name == 'posix': opt.add_argument('--headless')
    opt.add_argument('--disable-dev-shm-usage')
    opt.add_argument('--no-sandbox')
    opt.page_load_strategy = 'none'
    driver = webdriver.Chrome(options=opt)
    driver.maximize_window()
    driver.get(server + request.module.endpoint)

    yield driver
    driver.quit()