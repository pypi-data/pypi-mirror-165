from enum import Enum
from selenium.webdriver.remote.webdriver import By


class AbbrevByMapper(Enum):
    '''
    Abbreviate allowable By type
    '''
    ID = By.ID
    XPATH = By.XPATH
    LINK = By.LINK_TEXT
    PLINK = By.PARTIAL_LINK_TEXT
    NAME = By.NAME
    TAG = By.TAG_NAME
    CLASS = By.CLASS_NAME
    CSS = By.CSS_SELECTOR

def map_by_type(by_type: str):
    '''
    Simply map AbbrevByMapper
    '''
    return AbbrevByMapper[by_type.upper()].value
