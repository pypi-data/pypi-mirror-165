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
def test_rosepon_page_clear_all_inputs(
    rosenium_driver_instance: rosenium_driver.RoseniumDriver
):
    test_page = page.TPLTemplateLPTPage(rosenium_driver_instance)

    test_page.page_act(actions.TPLTemplateLPTActions.INPUT_DUMMY_TO_SEARCH_BOX)

    assert test_page.page_find(items.TPLTemplateLPTItems.INPUT_SEARCH).get_attribute("value") == "dummy"

    test_page.clear_all_inputs(items.TPLTemplateLPTItems.INPUT_SEARCH)

    assert test_page.page_find(items.TPLTemplateLPTItems.INPUT_SEARCH).get_attribute("value") == ""