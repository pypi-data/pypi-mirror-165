import logging
import pdb
import platform
import sys
from pathlib import Path
from typing import Optional, Union

import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chromium.webdriver import ChromiumDriver
from selenium.webdriver.common.options import ArgOptions as ArgOptions
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.ie.service import Service as IEService
from selenium.webdriver.remote.webelement import WebElement
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.core.driver import Driver
from webdriver_manager.core.http import WDMHttpClient
from webdriver_manager.firefox import GeckoDriver, GeckoDriverManager
from webdriver_manager.microsoft import IEDriverManager

try:
    from appium.webdriver.webdriver import WebDriver

    HAVE_APPIUM = True
except ImportError:
    from selenium.webdriver.remote.webdriver import WebDriver

__all__ = ["debugger", "get_webdriver", "session"]

from sys import exit, version_info

wdm_logger = logging.getLogger("WDM")
wdm_logger.setLevel(logging.ERROR)

logger = logging.getLogger(__name__)

if not all([version_info.major == 3, version_info.minor >= 9]):
    msg = """
    webdriver_helper: Python version should >=3.9，
    If you need to be compatible with special scenarios,
    please contact the developer for paid customization. """
    print(msg)
    logger.critical(msg)
    exit(-1)


# fix a bug
Driver.auth_header = None

session = requests.session()
WDMHttpClient.get = session.get


def get_geckodriver_manager():
    base_url = "https://registry.npmmirror.com/-/binary/geckodriver"

    def _get_latest_release_version(self):
        resp = requests.get(base_url)
        driver_list = resp.json()
        driver_list.sort(key=lambda x: x["date"])
        latest_driver = driver_list[-1]
        return latest_driver["name"][:-1]

    def _get_url(self) -> str:
        name = (
            f"{self.get_name()}-{self.get_version()}-{self.get_os_type()}{'-aarch64' if (self.get_os_type() == 'macos' and not platform.processor() == 'i386') else ''}"
            + ".zip"
        )
        url = f"{base_url}/{self.get_version()}/{name}"
        return url

    GeckoDriver.get_url = _get_url
    GeckoDriver.get_latest_release_version = _get_latest_release_version

    return GeckoDriverManager()


def get_chrome_manager(version=None):
    base_url = "https://registry.npmmirror.com/-/binary/chromedriver"
    latest_release_url = base_url + "/LATEST_RELEASE"

    if version:
        version = requests.get(latest_release_url + "_" + str(version)).text
    else:
        version = "latest"

    return ChromeDriverManager(
        version=version,
        url=base_url,
        latest_release_url=latest_release_url,
    )


def get_remote_webdriver(
    url,
    options: Optional[ArgOptions] = None,
    capabilities: dict = None,
) -> WebDriver:
    """
    启动selenium grid 或appium 的远端设备
    :param url: 远程hub地址
    :param options: 浏览器选项
    :param capabilities: 远端设备启动参数
    :return:
    """

    if not options and not capabilities:
        msg = f"启动远程浏览器时，以下参数必须有一个不为空：options 或 capabilities : {locals()}"

        logger.error(msg)
        raise ValueError(msg)

    if HAVE_APPIUM:
        return WebDriver(url, desired_capabilities=capabilities)
    return WebDriver(url, options=options, desired_capabilities=capabilities)


def get_webdriver(
    browser="chrome",
    version=None,
    options: Optional[ArgOptions] = None,
    service_args: dict = None,
    capabilities: dict = None,
) -> WebDriver:
    """
    自动就绪selenium，目前只支持Chrome 和 FireFox
    1. 下载浏览器驱动
    2. 实例化Service
    3. 实例化WebDriver
    :param browser: 浏览器类型
    :param version: 浏览器版本
    :param options: 浏览器选项
    :param service_args: service 实例化的参数
    :param capabilities: grid 的启动参数
    :return:
    """

    WebElement.upload_by_drop = upload_by_drop
    service_args = service_args or {}
    browser = browser.lower()

    if browser.startswith("http"):
        return get_remote_webdriver(
            browser,
            options=options,
            capabilities=capabilities,
        )

    elif browser == "chrome":
        _path = get_chrome_manager(version=version).install()
        service_args.update(executable_path=_path)
        return webdriver.Chrome(
            service=ChromeService(**service_args),
            options=options,
        )

    elif browser == "firefox":
        _path = get_geckodriver_manager().install()
        service_args.update(executable_path=_path)
        return webdriver.Firefox(
            service=FirefoxService(**service_args),
            options=options,
        )

    elif browser == "ie":
        _path = IEDriverManager().install()
        service_args.update(executable_path=_path)
        return webdriver.Ie(
            service=IEService(**service_args),
            options=options,
        )


def debugger(driver):
    """
    进入调试模式，为浏览器和python设置断言
    :param driver: WebDriver实例
    :return:
    """

    if not isinstance(driver, ChromiumDriver):
        logger.warning(
            f"The driver is not a Chromium kernel, and debugger cannot be used temporarily. ({driver=})"
        )
        return
    driver.execute_cdp_cmd("Debugger.enable", {})
    driver.execute_script("setTimeout('debugger', 0.1 * 1000)")

    class MyPdb(pdb.Pdb):
        def do_continue(self, arg: str):
            driver.execute_cdp_cmd("Debugger.disable", {})
            logger.warning("Chrome is exiting debug mode !")
            return super().do_continue(arg)

        do_c = do_cont = do_continue

        def __del__(self):
            logger.warning("Python is exiting debug mode !")

    msg = "Now in debug mode, Python and Chrome are suspended !"
    my_pdb = MyPdb()
    logger.warning(msg)
    my_pdb.set_trace(sys._getframe().f_back)


def upload_by_drop(
    target_element: WebElement,
    file_path: Union[str, Path],
) -> None:
    """
    实现文件的拖拽上传
    :param file_path: 文件绝对路径
    :param target_element: 接收拖拽的目标元素
    :return:
    """
    driver = target_element.parent
    file_path = Path(file_path).absolute()  # 必须相对路径转绝对路径
    js_path = Path(__file__).parent / "upload_by_drop.js"
    file_abs_path = str(file_path)  # 必须使用字符串

    if not file_path.exists():
        raise ValueError(f"File does not exist: path{file_abs_path}")
    if not file_path.is_file():
        raise ValueError(f"File is not a file: path={file_abs_path}")

    ele_input: WebElement = driver.execute_script(
        js_path.read_text("utf-8"),
        target_element,
        0,
        0,
    )
    ele_input.send_keys(file_abs_path)
