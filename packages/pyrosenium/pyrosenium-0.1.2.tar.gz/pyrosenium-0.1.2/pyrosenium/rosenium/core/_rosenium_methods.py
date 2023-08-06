from enum import Enum
import platform
from typing import List, Tuple, Union
from selenium.webdriver.remote.webdriver import WebDriver, WebElement
# from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains

from . import _rosenium_abbrev_mapper


OS = platform.system()


class RoseniumMethods(WebDriver):
    '''
    Useful predefined methods for using selenium
    '''
    def __init__(self):
        super().__init__()
        self.action_chain = None

    def r_find_ele(self: WebDriver, by_type: str, locator: str, index: int=None) -> WebElement:
        '''
        Shortand for find_element
        '''
        if index is not None:
            return self.find_elements(_rosenium_abbrev_mapper.map_by_type(by_type), locator)[index]
        return self.find_element(_rosenium_abbrev_mapper.map_by_type(by_type), locator)

    def r_find_eles(self: WebDriver, by_type: str, locator: str) -> List[WebElement]:
        '''
        Shortand for find_elements
        '''
        return self.find_elements(_rosenium_abbrev_mapper.map_by_type(by_type), locator)

    def r_scroll(self: WebDriver, scroll_by: Tuple[int, int]) -> None:
        '''
        Shortand for js scrollBy
        '''
        script = f'''
            window.scrollBy({scroll_by[0]}, {scroll_by[1]})
        '''
        self.execute_script(script)

    def r_initialize_action_chain(self) -> ActionChains:
        '''
        Shortand for ActionChains
        '''
        self.action_chain = ActionChains(self)

    def r_perform_action_chain(self, reserve=False) -> None:
        '''
        Shortand for performing ActionChains
        '''
        self.action_chain.perform()
        if not reserve:
            self.action_chain = None

    def r_clear_text_input(self: WebDriver, element: Union[WebElement, List[WebElement]]) -> None:
        '''
        Clear input of a text field, ignoring input or js fillable element
        '''
        if not isinstance(element, list):
            element = [element]
        for ele in element:
            ele.click()
            if OS != "Linux" and OS != "Windows":
                ele.send_keys(Keys.COMMAND + 'a')
            else:
                ele.send_keys(Keys.CONTROL + 'a')
            ele.send_keys(Keys.DELETE)


    # under development
    # def _wait_until(ec_func):

    #     def _wait_until_wrapper(*args, **kwargs) -> Tuple[bool, Any]:
    #         wait_time = kwargs.get("wait_time", 5)
    #         wait = WebDriverWait(args[0], wait_time)
    #         try:
    #             ec_res = ec_func(*args, wait, **kwargs)
    #             return (True, ec_res)
    #         except:
    #             return (False, None)

    #     return _wait_until_wrapper

    # @_wait_until
    # def until_visible(self, by_type: str, locator: str, wait: WebDriverWait):
    #     return wait.until(EC.visibility_of_element_located((rosenium_abbrev_mapper._map_by_type(by_type), locator)))
