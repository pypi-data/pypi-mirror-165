from pyrosenium.rosepom.helpers.rosenium_find_elements_methods import RFEM
from pyrosenium.rosepom.core import rosepom


class TPLTemplateLPTItems(rosepom.Items):
    '''
    Contains find methods and locators
    '''
    # EXAMPLE_ITEM = (RFEM.FIND, ["css", "div", 0])
    HEADER = (RFEM.FIND, ["id", "Welcome_to_Wikipedia"])
    WIKI_HREF = (RFEM.FIND, ["css", "a[href='/wiki/Wikipedia']"])
    WIKI_HEADER = (RFEM.FIND, ["id", "firstHeading"])
    INPUT_SEARCH = (RFEM.FIND, ["css", "input.vector-search-box-input"])