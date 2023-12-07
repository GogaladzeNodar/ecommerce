import pytest

from selenium import webdriver 
from selenium.webdriver.chrome.options import Options

@pytest.fixture(scope="function")
def chrome_browser_instance(request):
    """
    provide a selenium webdriven instance  
    """
    options = Options()
    options.headless = False
    browser = webdriver.Chrome(options=options)
    yield browser
    browser.close()
    