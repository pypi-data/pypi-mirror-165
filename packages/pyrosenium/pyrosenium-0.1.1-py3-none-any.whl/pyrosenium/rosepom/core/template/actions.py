from pyrosenium.rosenium.core import rosenium_driver
from pyrosenium.rosepom.core import rosepom

from . import page
from . import items



def example_action(self: page.TPLTemplateLPTPage, page_driver: rosenium_driver.RoseniumDriver):
    '''
    Example use of action_chain
    '''
    # page_driver.r_initialize_action_chain()
    # page_driver.action_chain.click(items.TemplateItems.EXAMPLE_ITEM)


class TPLTemplateLPTActions(rosepom.Actions):
    '''
    Register actions here Tuple[Callable, List (arguments), is_r_perform, is_reserve]
    Different actions with different input strategies
    '''
    # EXAMPLE_NO_ACTION_CHAIN = (example_action, [], False)
    # EXAMPLE_ACTION_CHAIN = (example_action, [], True, False)
