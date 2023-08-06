from typing import Any
from selenium.webdriver.remote.webdriver import By

from pyrosenium.rosenium.core import rosenium_driver

from ... import testenv_configs


# TODO make this functional
class DefaultRoseniumDriverDecorator:
    '''
    Setting up default rosenium driver
    '''
    def __init__(self, default_page: str="https://en.wikipedia.org/wiki/Main_Page") -> None:
        self.default_page = default_page

    def __call__(self, test_func) -> Any:
        def build_rosenium_driver_wrapper(*args, **kwargs):
            rosenium_driver_instance = rosenium_driver.build_rosenium_driver(
                testenv_configs.build_default_base_driver()
            )
            rosenium_driver_instance.get(self.default_page)

            test_func(rosenium_driver_instance)

        return build_rosenium_driver_wrapper


@DefaultRoseniumDriverDecorator()
def test_build_rosenium_driver(rosenium_driver_instance: rosenium_driver.RoseniumDriver):
    '''
    test_build_rosenium_driver
    '''
    assert rosenium_driver_instance.find_element(By.ID, "Welcome_to_Wikipedia").text \
        == "Welcome to Wikipedia"
