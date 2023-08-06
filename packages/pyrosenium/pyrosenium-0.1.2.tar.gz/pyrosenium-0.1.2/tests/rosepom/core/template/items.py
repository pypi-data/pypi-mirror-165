from pyrosenium.rosepom.helpers.rosenium_find_elements_methods import RFEM
from pyrosenium.rosepom.core import rosepom


class TPLTemplateLPTItems(rosepom.Items):
    '''
    Contains find methods and locators
    '''
    # EXAMPLE_ITEM = (RFEM.FIND, ["css", "div", 0])
    
    # Wiki Page
    HEADER = (RFEM.FIND, ["id", "Welcome_to_Wikipedia"])
    WIKI_HREF = (RFEM.FIND, ["css", "a[href='/wiki/Wikipedia']"])
    WIKI_HEADER = (RFEM.FIND, ["id", "firstHeading"])
    INPUT_SEARCH = (RFEM.FIND, ["css", "input.vector-search-box-input"])

    # select_option
    SELECT_CAR = (RFEM.FIND, ["css", "select.form-select", 0])
    OPTION_CAR = (RFEM.FIND, ["css", "option[value='1']", 0])

    # check_uncheck_checkbox_declaration
    CHECKBOX_UNCHECKED = (RFEM.FIND, ["css", ".form-check-input.mt-0[type='checkbox']"])
    CHECKBOX_CHECKED = (RFEM.FIND, ["css", ".form-check-input.mt-0[type='checkbox']"])  # same