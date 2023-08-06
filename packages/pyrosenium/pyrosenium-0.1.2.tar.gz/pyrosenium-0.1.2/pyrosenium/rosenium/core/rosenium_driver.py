from typing import Union
from selenium.webdriver.remote.webdriver import WebDriver

from . import _rosenium_methods
from ..helpers import base_driver


def _inject_extra_methods(custom_rosenium_methods: _rosenium_methods.RoseniumMethods =_rosenium_methods.RoseniumMethods) -> None:
    '''
    Inject extra methods to base_driver_instance
    '''
    extra_method_list = [
        func for func in dir(custom_rosenium_methods) \
            if callable(getattr(custom_rosenium_methods, func)) and \
                func.startswith("r_")
    ]
    for method in extra_method_list:
        setattr(WebDriver, method, getattr(custom_rosenium_methods, method))


# Public
class RoseniumDriver(_rosenium_methods.RoseniumMethods):
    '''
    for typing
    '''


class RoseniumDriverParams(base_driver.BaseDriverParams):
    '''
    for typing
    '''


def build_rosenium_driver(
    base_driver_recipe: Union[RoseniumDriverParams, WebDriver],
    custom_rosenium_methods: _rosenium_methods.RoseniumMethods =_rosenium_methods.RoseniumMethods
) -> RoseniumDriver:
    '''
    Build rosenium_driver from recipe
    '''
    _inject_extra_methods(custom_rosenium_methods)

    if not isinstance(base_driver_recipe, WebDriver):
        rosenium_driver_instance = base_driver.build_base_driver(base_driver_recipe)
    else:
        rosenium_driver_instance = base_driver_recipe

    return rosenium_driver_instance
