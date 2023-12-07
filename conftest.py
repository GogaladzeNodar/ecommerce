# import pytest
# from selenium.webdriver.common.keys import Keys

# @pytest.mark.selenium
# def test_dashboard_admin_login():
    
pytest_plugins = [
    "ecommerce.tests.selenium",
    "ecommerce.tests.fixtures",
]
