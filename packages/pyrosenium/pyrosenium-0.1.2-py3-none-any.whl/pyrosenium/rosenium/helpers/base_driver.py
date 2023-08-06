from dataclasses import dataclass
from enum import Enum
from typing import List, Tuple
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver import Chrome, Edge, Firefox
from selenium.webdriver.common.service import Service
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.common.options import ArgOptions
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.edge.options import Options as EdgeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from webdriver_manager.core.manager import DriverManager
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.microsoft import EdgeChromiumDriverManager


@dataclass
class BaseDriverParams:
    '''
    Receipe for building selenium web driver
    '''
    brand: str
    executable_path: str
    implicit_wait: int
    extension_path_list: List[str]
    argument_list: List[str]
    use_driver_manager: bool = False
    window_size: Tuple[int, int] = None


class _DriverBrandEnum(Enum):
    '''
    Different driver brands and typing
    '''
    CHROME = (
        ChromeDriverManager, Chrome, ChromeService, ChromeOptions
    )
    EDGE = (
        EdgeChromiumDriverManager, Edge, EdgeService, EdgeOptions
    )
    FIREFOX = (
        GeckoDriverManager, Firefox, FirefoxService, FirefoxOptions
    )


def _select_driver_from_brand(brand: str) -> Tuple[DriverManager, WebDriver, Service, ArgOptions]:
    '''
    Simply get driver brands and typing
    '''
    return _DriverBrandEnum[brand.upper()].value

def _download_driver(driver_manager_cls: DriverManager, executable_path: str) -> str:
    '''
    Download executable into folder
    '''
    driver_manager: DriverManager = driver_manager_cls(
        path=executable_path
    )
    return driver_manager.install()

def _initialize_base_driver(
    web_driver_cls,
    service_cls,
    options_cls,
    base_driver_params: BaseDriverParams
) -> WebDriver:
    '''
    Initialize selenium driver
    '''
    service: Service = service_cls(executable_path=base_driver_params.executable_path)
    options: ArgOptions = options_cls()

    if base_driver_params.argument_list:
        for argument in base_driver_params.argument_list:
            options.add_argument(argument)

    if base_driver_params.extension_path_list:
        for extension in base_driver_params.extension_path_list:
            options.add_extension(extension)

    base_driver: WebDriver =  web_driver_cls(
        service=service,
        options=options
    )

    if base_driver_params.window_size is not None:
        base_driver.set_window_size(
            base_driver_params.window_size[0],
            base_driver_params.window_size[1]
        )

    if base_driver_params.implicit_wait is not None:
        base_driver.implicitly_wait(base_driver_params.implicit_wait)

    return base_driver


# Public
def build_base_driver(base_driver_params: BaseDriverParams) -> WebDriver:
    '''
    Build base_driver from recipe
    '''
    [
        driver_manager_cls,
        web_driver_cls,
        service_cls,
        options_cls
    ] = _select_driver_from_brand(base_driver_params.brand)

    if base_driver_params.use_driver_manager:
        base_driver_params.executable_path = _download_driver(
            driver_manager_cls,
            base_driver_params.executable_path
        )

    return _initialize_base_driver(web_driver_cls, service_cls, options_cls, base_driver_params)
