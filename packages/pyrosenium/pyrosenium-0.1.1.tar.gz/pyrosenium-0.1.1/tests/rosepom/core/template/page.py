from typing import List

from pyrosenium.rosenium.core import rosenium_driver
from pyrosenium.rosepom.core import rosepom

from . import items


class TPLTemplateLPTPage(rosepom.Page):
    '''
    Page object
    '''
    def __init__(
        self,
        page_driver: rosenium_driver.RoseniumDriver,
        page_items = items.TPLTemplateLPTItems,
        entry_url_args: List = None
    ) -> None:
        super().__init__(page_driver, page_items, entry_url_args)

        # Disable auto-load by default
        # self.page_driver.get(self.get_entry_url(entry_url_args))


    ### Override instance methods below
    def get_entry_url(self, entry_url_args) -> str:
        '''
        Override instance get_entry_url here
        '''
        return "https://en.wikipedia.org/wiki/Main_Page"

    # def page_find

    # def page_act

    # def extract_page_driver


    ### Custom instance methods below
