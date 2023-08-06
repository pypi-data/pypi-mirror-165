from pyrosenium.rosenium.core import rosenium_driver
from pyrosenium.rosepom.core import rosepom

from . import page
from . import items


def click_wiki_href_action_chain(self: page.TPLTemplateLPTPage, page_driver: rosenium_driver.RoseniumDriver, wiki_href: rosenium_driver._rosenium_methods.WebElement):
    '''
    Example use of action_chain
    '''
    page_driver.r_initialize_action_chain()
    page_driver.action_chain.click(wiki_href)

def click_wiki_href_no_action_chain(self: page.TPLTemplateLPTPage, page_driver: rosenium_driver.RoseniumDriver):
    '''
    click_wiki_href_no_action_chain
    '''
    self.page_find(items.TPLTemplateLPTItems.WIKI_HREF).click()

def input_dummy_to_search_box(self: page.TPLTemplateLPTPage, page_driver: rosenium_driver.RoseniumDriver, input_search: rosenium_driver._rosenium_methods.WebElement):
    '''
    input_dummy_to_search_box
    '''
    input_search.send_keys("dummy")


class TPLTemplateLPTActions(rosepom.Actions):
    '''
    Register actions here Tuple[Callable, List (arguments)]
    Different actions with different input strategies
    '''
    # EXAMPLE_ACTION = (example_action, [], False)
    # EXAMPLE_ACTION = (example_action, [], True, False)
    CLICK_WIKI_HREF_ACTION_CHAIN = (
        click_wiki_href_action_chain, [items.TPLTemplateLPTItems.WIKI_HREF], True
    )

    CLICK_WIKI_HREF_NO_ACTION_CHAIN = (
        click_wiki_href_no_action_chain, [], False
    )

    INPUT_DUMMY_TO_SEARCH_BOX = (
        input_dummy_to_search_box, [items.TPLTemplateLPTItems.INPUT_SEARCH], False
    )