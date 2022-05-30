"""
`conftest.py` and `pylenium.json` files should stay at Workspace Root.

conftest.py
    Although this file is editable, you should only change its contents if you know what you are doing.
    Instead, you can create your own conftest.py file in the folder where you store your tests.

pylenium.json
    You can change the values, but DO NOT touch the keys or you will break the schema.

py
    The only fixture you really need from this is `py`. This is the instance of Pylenium for each test.

Examples:
    def test_go_to_google(py):
        py.visit('https://google.com')
        assert 'Google' in py.title()
"""

import json
import logging
import os
import shutil
import sys
from pathlib import Path

import allure
import pytest
from pylenium.config import PyleniumConfig, TestCase
from pylenium.driver import Pylenium
from pytest_reportportal import RPLogger, RPLogHandler

from base.api.base import health_check
from models.utils.users.seeders import setup_role_patterns
from models.utils.ztool.elements import upload_default_textbook_attachment
from settings import PROJECT_ROOT, DEBUG
from utils.formatters.slack import save_result_status
from utils.ui.components.component import Py
from utils.ui.constants import DOWNLOAD_PATH

pytest_plugins = [
    'utils.fixtures.api.users.user',
    'utils.fixtures.api.users.user_role',
    'utils.fixtures.api.users.group',
    'utils.fixtures.api.users.group_user',
    'utils.fixtures.api.users.objective',
    'utils.fixtures.api.users.resource_library',
    'utils.fixtures.api.users.role_pattern',
    'utils.fixtures.api.users.tenant',
    'utils.fixtures.api.users.activity',
    'utils.fixtures.api.users.tenant_settings',
    'utils.fixtures.api.ztool.workflow',
    'utils.fixtures.ui.course',
    'utils.fixtures.ui.workflow'
]


@pytest.fixture(scope="session")
def rp_logger(request):
    """Report Portal Logger"""
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)
    # Create handler for Report Portal if the service has been
    # configured and started.
    if hasattr(request.node.config, 'py_test_service'):
        # Import Report Portal logger and handler to the test module.
        logging.setLoggerClass(RPLogger)
        rp_handler = RPLogHandler(request.node.config.py_test_service)
        # Add additional handlers if it is necessary
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(logging.INFO)
        logger.addHandler(console_handler)
    else:
        rp_handler = logging.StreamHandler(sys.stdout)
    # Set INFO level for Report Portal handler.
    rp_handler.setLevel(logging.INFO)
    return logger


@pytest.fixture(scope='session', autouse=True)
def test_run(request) -> str:
    """Creates the `/test_results` directory to store the results of the Test Run.

    Returns:
        The `/test_results` directory as a filepath (str).
    """
    session = request.node
    test_results_dir = f'{PROJECT_ROOT}/test_results'

    if os.path.exists(test_results_dir):
        # delete /test_results from previous Test Run
        shutil.rmtree(test_results_dir, ignore_errors=True)

    try:
        # race condition can occur between checking file existence and
        # creating the file when using pytest with multiple workers
        Path(test_results_dir).mkdir(parents=True, exist_ok=True)
    except (FileExistsError, FileNotFoundError):
        pass

    for test in session.items:
        try:
            # make the test_result directory for each test
            Path(f'{test_results_dir}/{test.name}').mkdir(parents=True, exist_ok=True)
        except (FileExistsError, OSError):
            pass

    return test_results_dir


@pytest.fixture(scope='session')
def py_config(request) -> PyleniumConfig:
    """Initialize a PyleniumConfig for each test

    1. This starts by deserializing the user-created pylenium.json from the Project Root.
    2. If that file is not found, then proceed with Pylenium Defaults.
    3. Then any CLI arguments override their respective key/values.
    """
    try:
        # 1. Load pylenium.json in Project Root, if available
        with open(f'{PROJECT_ROOT}/pylenium.json') as file:
            settings = json.load(file)
            if not DEBUG:
                settings['driver']['options'] = [
                    *settings['driver']['options'],
                    '--headless',
                    '--disable-extensions',
                    '--disable-gpu'
                ]

        download_path = DOWNLOAD_PATH if DEBUG else '/home/seluser/downloads'
        settings['driver']['experimental_options'] = [
            {'prefs': {'download.default_directory': download_path}}
        ]
        config = PyleniumConfig(**settings)
    except FileNotFoundError:
        # 2. pylenium.json not found, proceed with defaults
        config = PyleniumConfig()

    # 3. Override with any CLI args/options
    # Driver Settings
    cli_remote_url = request.config.getoption('--remote_url')
    if cli_remote_url:
        config.driver.remote_url = cli_remote_url

    cli_browser_options = request.config.getoption('--options')
    if cli_browser_options:
        config.driver.options = [option.strip() for option in cli_browser_options.split(',')]

    cli_browser = request.config.getoption('--browser')
    if cli_browser:
        config.driver.browser = cli_browser

    cli_capabilities = request.config.getoption('--caps')
    if cli_capabilities:
        # --caps must be in '{"name": "value", "boolean": true}' format
        # with double quotes around each key. booleans are lowercase.
        config.driver.capabilities = json.loads(cli_capabilities)

    cli_page_wait_time = request.config.getoption('--page_load_wait_time')
    if cli_page_wait_time and cli_page_wait_time.isdigit():
        config.driver.page_load_wait_time = int(cli_page_wait_time)

    # Logging Settings
    cli_screenshots_on = request.config.getoption('--screenshots_on')
    if cli_screenshots_on:
        shots_on = True if cli_screenshots_on.lower() == 'true' else False
        config.logging.screenshots_on = shots_on

    cli_extensions = request.config.getoption('--extensions')
    if cli_extensions:
        config.driver.extension_paths = [ext.strip() for ext in cli_extensions.split(',')]

    return config


@pytest.fixture(scope='function')
def test_case(test_run, py_config, request) -> TestCase:
    """
    Manages data pertaining to the currently running Test Function or Case.

        * Creates the test-specific logger.

    Args:
        test_run: The Test Run (or Session) this test is connected to.

    Returns:
        An instance of TestCase.
    """
    test_name = request.node.name
    test_result_path = f'{test_run}/{test_name}'
    py_config.driver.capabilities.update({'name': test_name})
    return TestCase(name=test_name, file_path=test_result_path)


@pytest.fixture(scope='function')
def py(test_case, py_config, request, rp_logger):
    """
    Initialize a Pylenium driver for each test.

    Pass in this `py` fixture into the test function.

    Examples:
        def test_go_to_google(py):
            py.visit('https://google.com')
            assert 'Google' in py.title()
    """
    py = Pylenium(py_config)
    Py.set_py(py)
    yield py
    try:
        if py_config.logging.screenshots_on:
            screenshot = py.screenshot(f'{test_case.file_path}/{request.node.name}.png')
            allure.attach.file(screenshot, name='Page', attachment_type=allure.attachment_type.PNG)
    except FileNotFoundError:
        pass

    finally:
        py.quit()


def pytest_addoption(parser):
    parser.addoption('--browser', action='store', default='', help='The lowercase browser name: chrome | firefox')
    parser.addoption('--remote_url', action='store', default='', help='Grid URL to connect tests to.')
    parser.addoption('--screenshots_on', action='store', default='', help="Should screenshots be saved? true | false")
    parser.addoption('--pylog_level', action='store', default='', help="Set the pylog_level: 'off' | 'info' | 'debug'")
    parser.addoption(
        '--options',
        action='store',
        default='',
        help='Comma-separated list of Browser Options. Ex. "headless, incognito"',
    )
    parser.addoption(
        '--caps',
        action='store',
        default='',
        help='List of key-value pairs. Ex. \'{"name": "value", "boolean": true}\'',
    )
    parser.addoption(
        '--page_load_wait_time',
        action='store',
        default='',
        help='The amount of time to wait for a page load before raising an error. Default is 0.',
    )
    parser.addoption(
        '--extensions', action='store', default='', help='Comma-separated list of extension paths. Ex. "*.crx, *.crx"'
    )


def pytest_sessionstart(session):
    health_check()
    setup_role_patterns()
    upload_default_textbook_attachment()


def pytest_sessionfinish(session, exitstatus):
    if not DEBUG:
        save_result_status(session.testsfailed, session.testscollected)
