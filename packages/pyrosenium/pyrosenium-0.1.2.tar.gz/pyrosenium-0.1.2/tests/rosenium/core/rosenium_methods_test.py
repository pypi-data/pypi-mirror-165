from pyrosenium.rosenium.core import rosenium_driver

from .rosenium_driver_test import DefaultRoseniumDriverDecorator


@DefaultRoseniumDriverDecorator()
def test_find_ele(rosenium_driver_instance: rosenium_driver.RoseniumDriver):
    '''
    test_find_ele
    '''
    assert rosenium_driver_instance.r_find_ele("id", "Welcome_to_Wikipedia").text \
        == "Welcome to Wikipedia"

    # TODO find some index > 0
    assert rosenium_driver_instance.r_find_ele("id", "Welcome_to_Wikipedia", 0).text \
        == "Welcome to Wikipedia"

@DefaultRoseniumDriverDecorator()
def test_find_eles(rosenium_driver_instance: rosenium_driver.RoseniumDriver):
    '''
    test_find_eles
    '''
    assert len(rosenium_driver_instance.r_find_eles("css", "div.mw-parser-output div.mp-box")) \
        == 5

@DefaultRoseniumDriverDecorator()
def test_scroll(rosenium_driver_instance: rosenium_driver.RoseniumDriver):
    '''
    test_scroll
    '''
    scroll_y = 1000
    rosenium_driver_instance.r_scroll((0, scroll_y))

    assert rosenium_driver_instance.execute_script("return window.pageYOffset") \
        == scroll_y

@DefaultRoseniumDriverDecorator()
def test_action_chain(rosenium_driver_instance: rosenium_driver.RoseniumDriver):
    '''
    test_action_chain
    '''
    rosenium_driver_instance.r_initialize_action_chain()
    rosenium_driver_instance.action_chain.pause(0)
    rosenium_driver_instance.r_perform_action_chain()
    # TODO assert something else
    assert True

@DefaultRoseniumDriverDecorator()
def test_clear_text_input(rosenium_driver_instance: rosenium_driver.RoseniumDriver):
    '''
    test_clear_text_input
    '''
    input_search = rosenium_driver_instance.r_find_ele("css", "input[name='search']")
    input_search.send_keys("TEST")
    assert input_search.get_attribute("value") \
        == "TEST"

    rosenium_driver_instance.r_clear_text_input(input_search)
    assert input_search.get_attribute("value") \
        == ""
