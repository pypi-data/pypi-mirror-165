import time
from enum import Enum
from typing import List, Union, Callable
from pyrosenium.rosenium.core import rosenium_driver
from pyrosenium.rosenium.core._rosenium_methods import WebElement


class Items(Enum):
    '''
    For typing Items
    (PFEM, [args])
    '''


class Actions(Enum):
    '''
    For typing Actions
    (Callable, [args])
    '''


class Page:
    '''
    Page object
    '''
    def __init__(
        self,
        page_driver: rosenium_driver.RoseniumDriver,
        page_items: Items,
        entry_url_args: List = None
    ) -> None:
        self.page_driver = page_driver
        self.page_items = page_items

        self.page_items_dict = {}

    def get_entry_url(self, entry_url_args):
        '''
        Visity entry page using entry_url_args is needed
        Requires override in instance method
        '''

    def page_find(self, item: Items, reserve=True) \
        -> Union[WebElement, List[WebElement]]:
        '''
        Find and set elements
        '''
        if len(item.value) > 2:
            raise ValueError(
                "Too many arguments, item should be a tuple with length of size 2 [method, locator]."
            )
        web_element = getattr(self.page_driver, item.value[0].value)(*item.value[1])
        if reserve:
            self.page_items_dict[item.name] = web_element
        return web_element

    def page_act(self, action: Actions) -> None:
        '''
        Perform action (chain)
        '''
        if not action.value[-2] and len(action.value) == 4:
            raise ValueError(
                "Too many arguments, non action_chain actions should only have three."
            )

        action_args = action.value[1]
        new_action_args = []
        for arg in action_args:
            if isinstance(arg, self.page_items):
                new_action_args.append(self.page_find(arg))
            else:
                new_action_args.append(arg)

        action.value[0](self, self.page_driver, *new_action_args)

        if action.value[2]:
            try:
                reserve = action.value[3]
            except IndexError as _:
                reserve = False
            self.page_driver.r_perform_action_chain(reserve)

    def input_text_fields(self, items: Items, input_data: dict):
        '''
        input_text_fields
        '''
        for key, value in input_data.items():
            if isinstance(value, Callable):
                value = value()
            self.page_find(items[key]).send_keys(value)


    def clear_all_inputs(self, *all_input_elements):
        '''
        Clear all text inputs
        '''
        for input_element in all_input_elements:
            ele = self.page_find(input_element)
            self.page_driver.r_clear_text_input(ele)

    def select_option(self, select_item: Items, option_item: Items, delay: float=1):
            '''
            select_option
            '''
            self.page_driver.r_scroll((0, 500))
            select_ele = self.page_find(select_item)
            time.sleep(delay)
            select_ele.click()
            time.sleep(delay)
            self.page_driver.r_scroll((0, 100))
            self.page_find(option_item).click()

    def check_uncheck_checkbox_declaration(
        self, checkbox_declaration_unchecked: Items = None, checkbox_declaration_checked: Items = None):
        '''
        check_uncheck_declaration
        '''
        if checkbox_declaration_unchecked is not None and checkbox_declaration_checked is not None:
            raise ValueError("Only one of checkbox_declaration_unchecked/ checkbox_declaration_checked should exist.")
        elif checkbox_declaration_unchecked is None and checkbox_declaration_checked is None:
            raise ValueError("Absence of checkbox_declaration_unchecked and checkbox_declaration_checked")
        if checkbox_declaration_unchecked is not None:
            self.page_find(checkbox_declaration_unchecked).click()
        elif checkbox_declaration_checked is not None:
            self.page_find(checkbox_declaration_checked).click()

    def extract_page_driver(self) -> rosenium_driver.RoseniumDriver:
        '''
        Simply get page_driver
        '''
        return self.page_driver