import time
from pyrosenium.rosenium.core import rosenium_driver

from .template import page
from .template import items
from .template import actions
from ...rosenium.core.rosenium_driver_test import DefaultRoseniumDriverDecorator


@DefaultRoseniumDriverDecorator()
def test_rosepom_page_action_action_chain(
    rosenium_driver_instance: rosenium_driver.RoseniumDriver
):
    '''
    test_rosepom
    '''
    test_page = page.TPLTemplateLPTPage(rosenium_driver_instance)
    assert test_page.page_find(items.TPLTemplateLPTItems.HEADER).text \
        == "Welcome to Wikipedia"

    test_page.page_act(actions.TPLTemplateLPTActions.CLICK_WIKI_HREF_ACTION_CHAIN)
    assert test_page.page_find(items.TPLTemplateLPTItems.WIKI_HEADER).text \
        == "Wikipedia"

@DefaultRoseniumDriverDecorator()
def test_rosepom_page_action_no_action_chain(
    rosenium_driver_instance: rosenium_driver.RoseniumDriver
):
    '''
    test_rosepom
    '''
    test_page = page.TPLTemplateLPTPage(rosenium_driver_instance)
    assert test_page.page_find(items.TPLTemplateLPTItems.HEADER).text \
        == "Welcome to Wikipedia"

    test_page.page_act(actions.TPLTemplateLPTActions.CLICK_WIKI_HREF_NO_ACTION_CHAIN)
    assert test_page.page_find(items.TPLTemplateLPTItems.WIKI_HEADER).text \
        == "Wikipedia"

@DefaultRoseniumDriverDecorator()
def test_rosepon_page_input_text_fields_then_clear_all_inputs(
    rosenium_driver_instance: rosenium_driver.RoseniumDriver
):
    test_page = page.TPLTemplateLPTPage(rosenium_driver_instance)
    input_data = {"INPUT_SEARCH": "dummy"}
    test_page.input_text_fields(items.TPLTemplateLPTItems, input_data)
    assert test_page.page_find(items.TPLTemplateLPTItems.INPUT_SEARCH).get_attribute("value") == "dummy"

    test_page.clear_all_inputs(items.TPLTemplateLPTItems.INPUT_SEARCH)
    assert test_page.page_find(items.TPLTemplateLPTItems.INPUT_SEARCH).get_attribute("value") == ""

@DefaultRoseniumDriverDecorator("https://getbootstrap.com/docs/5.0/forms/select/")
def test_rosepon_page_select_option(
    rosenium_driver_instance: rosenium_driver.RoseniumDriver
):
    test_page = page.TPLTemplateLPTPage(rosenium_driver_instance)
    time.sleep(1)
    test_page.select_option(items.TPLTemplateLPTItems.SELECT_CAR, items.TPLTemplateLPTItems.OPTION_CAR)
    assert test_page.page_find(items.TPLTemplateLPTItems.SELECT_CAR).get_attribute("value") == "1"

# TODO update this (requires visual checking at the moment).
@DefaultRoseniumDriverDecorator("https://getbootstrap.com/docs/5.0/forms/input-group/#checkboxes-and-radios")
def test_check_uncheck_checkbox_declaration(
    rosenium_driver_instance: rosenium_driver.RoseniumDriver
):
    test_page = page.TPLTemplateLPTPage(rosenium_driver_instance)
    time.sleep(1)
    test_page.check_uncheck_checkbox_declaration(items.TPLTemplateLPTItems.CHECKBOX_UNCHECKED, None)
    time.sleep(1)
    test_page.check_uncheck_checkbox_declaration(None, items.TPLTemplateLPTItems.CHECKBOX_CHECKED)
    time.sleep(1)