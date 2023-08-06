# Pyrosenium
## Introduction
This project/ framework is developed to support software QA engineer to facilitate their jobs. It provides two packages -- `rosenium` and `rosepom`.

### Rosenium
The `rosenium` package provides a short cut to construct a Selenium WebDriver class with help of a dataclass `RoseniumDriverParams`. This dataclass provides crucial hints for setting up a WebDriver. The packae method -- `build_rosenium_driver` makes use of `RoseniumDriverParams` to construct a WebDriver instance. It at the same time injects custom shorthand methods to the WebDriver class. This aims to help developers to quickly write scripts that require WebDriver.

You can create your own `rosenium_driver` with your custom `RoseniumMethods` by creating a `RoseniumMethods` class that is in line with the default one inside `_rosenium_methods.py`, and then passing it as an argument to the `build_rosenium_driver` method.

### Rosepom
The `rosepom` package provides a command to quickly generate pom templates. Simply run `create-rosepom-app $app_name` to create page specific pom based on the package template.
```
Template directory:
$your_folder
  |
  |__ $app_name
    |
    |__ __init__.py
    |__ actions.py
    |__ data.py
    |__ items.py
    |__ page.py
```
The template folder should include the following 4 files.
- actions.py:
  - You may define action functions in this page, and then register them inside $app_nameActions as indicated in the EXAMPLE_ACTION.
- data.py
  - Any data object, such as dict, list, etc.
  - You may put different data strategies here for different testing cases.
- items.py
  - You may define page items such as a div, a button, etc.
- page.py
  - Contains a $app_namePage object to be called in your script. You can interact with this object to use items and page actions as mentioned respectively in the $app_nameItems and $app_nameActions classes.

If you have custom `RoseniumMethods` and would like to use the custom methods on the `Page` object's page_find method, you can create an Enum class that includes the methods name; then importing and using it in the `Items` and `Actions` objects as a shortcut. Please see the source codes for more details.


## Examples
### Using rosenium_driver
Please see ~/../tests/rosenium/core/*
### Using rospom model
Please see ~/../tests/rosepom/core/*

## Diagrams
### Class diagram
```mermaid
classDiagram

  RoseniumDriver .. BaseDriverParams
  

  BaseDriverParams .. _DriverBrandEnum

  class BaseDriverParams{
    + brand: str
    + executable_path: str`
    + implicit_wait: int
    + extension_path_list: List[str]
    + argument_list: List[str]
    + use_driver_manager: bool
    + window_size: Tuple[int, int]
  }
  class _DriverBrandEnum{
    + CHROME: Tuple[DriverManager, WebDriver, Service, ArgOptions]
    + EDGE: Tuple[DriverManager, WebDriver, Service, ArgOptions]
    + FIREFOX: Tuple[DriverManager, WebDriver, Service, ArgOptions]
  }


  BaseDriverParams <|-- RoseniumDriverParams
  RoseniumMethods <|-- RoseniumDriver
  RoseniumMethods ..> AbbrevByMapper
  WebDriver <|-- RoseniumMethods

  class WebDriver
  
  class AbbrevByMapper{
    ID: By
    XPATH: By
    LINK: By
    PLINK: By
    NAME: By
    TAG: By
    CLASS: By
    CSS: By
  }

  class RoseniumDriver
  class RoseniumDriverParams

  class RoseniumMethods{
    +r_find_ele(by_type, locator, index) WebElement
    +r_find_eles(by_type, locator) List(WebElement)
    +r_scroll(scroll_by)
    +r_initialize_action_chain() ActionChains
    +r_perform_action_chain(reserve)
    +r_clear_text_input(element)
  }


  Page *-- RoseniumDriver
  Page *-- Actions
  Page *-- Items
  RoseniumFindElementMethods --> RoseniumMethods

  class Page{
    + page_driver: rosenium_driver.RoseniumDriver,
    + page_items: Items,
    + entry_url_args: List
    +get_entry_url(entry_url_args) str
    +page_find(item, reserve) WebElement, Lise(WebElement)
    +page_act(action)
    +extract_page_driver() RoseniumDriver
  }
  class Actions{
    EXAMPLE_ACTION: Tuple(example_action, List, bool, bool)
  }
  class Items{
    HEADER = Tuple(RFEM, List(By, Locator))
  }
  class RoseniumFindElementMethods{
    FIND: str
    FINDS: str
  }
```
## Rosepom flowchart
```mermaid
flowchart TB
  id1(cd pom folder) -- run create-rosepom-app $app_name --> id2(rename classes inside items, page, actions)
  id2 --> id3-1(add locators in items.py) & id3-2(add page actions in actions.py) & id3-3(add different data strategies in data.py) --> id4(add page specific functions in page.py)
  id4 --> id5(add main/ test functions which interact with the above elements)
  id5 -- build rosenium_driver with RoseniumDriverParams\n create Page instance --> id7(run the main/ test.py)
  id7 -- repeat with other pages --> id1

```
