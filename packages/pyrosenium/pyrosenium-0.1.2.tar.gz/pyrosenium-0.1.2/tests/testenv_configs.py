import os
import screeninfo

from pyrosenium.rosenium.helpers import base_driver


ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

MONITOR_SIZE = screeninfo.get_monitors()[0]

def build_default_base_driver_params():
    '''
    Default params for setting up base_driver
    '''
    return base_driver.BaseDriverParams(
        brand = "chrome",
        executable_path = f"{ROOT_DIR}/tmp_download/driver",
        implicit_wait = 0,
        extension_path_list = [],
        argument_list=[],
        # argument_list = ["--headless"],
        use_driver_manager = True,
        window_size = (int(MONITOR_SIZE.width * 0.5), int(MONITOR_SIZE.height * 0.95)),
    )

def build_default_base_driver():
    '''
    Use build_default_base_driver_params to get base_driver
    '''
    return base_driver.build_base_driver(build_default_base_driver_params())
