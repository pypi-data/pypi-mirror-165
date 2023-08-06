from selenium.webdriver.common.by import By

from ... import testenv_configs


def test_build_base_driver():
    '''
    test_build_base_driver
    '''
    base_driver_instance = testenv_configs.build_default_base_driver()
    base_driver_instance.get("https://en.wikipedia.org/wiki/Main_Page")

    assert base_driver_instance.find_element(By.ID, "Welcome_to_Wikipedia").text \
        == "Welcome to Wikipedia"
