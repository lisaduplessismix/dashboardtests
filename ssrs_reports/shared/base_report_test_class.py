import os
import time
import json
import base64
import requests
import unittest
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait


# import configuration
selenium_host = os.getenv('SELENIUM_HOST')
webdriver_url = f"{selenium_host}/wd/hub"
dynamix_url = os.getenv('DYNAMIX_URL')
dynamix_user = os.getenv('DYNAMIX_USER')
dynamix_password = os.getenv('DYNAMIX_PASSWORD')

DEFAULT_TIMEOUT = 60


class BaseReportTest(unittest.TestCase):

    def __init__(self, methodName: str = ...) -> None:
        super().__init__(methodName)

        self.downloaded_reports_folder = "./downloaded_reports/"
        os.makedirs(self.downloaded_reports_folder, exist_ok=True)

    @classmethod
    def setUpClass(cls):
        """
        This function runs once before any of the tests in the class runs
        """
        super(BaseReportTest, cls).setUpClass()
        desired_capabilities = {
            'browserName': 'chrome',
            'goog:chromeOptions': {
                'args': [
                ],
                'prefs': {
                    'download.default_directory': "/home/seluser/",
                    'download.directory_upgrade': True,
                    'download.prompt_for_download': False,
                    'plugins.always_open_pdf_externally': True,
                    'safebrowsing_for_trusted_sources_enabled': False,
                    'safebrowsing.enabled': False
                }
            }
        }
        cls._clear_sessions()
        cls.browser = webdriver.Remote(webdriver_url, desired_capabilities=desired_capabilities)
        cls.browser.set_window_position(0, 0)
        cls.browser.set_window_size(1920, 1200)

        # navigate to dynamix and log in
        cls._navigate_to_dynamix_and_login(cls)

    @classmethod
    def tearDownClass(cls):
        """
        This function runs once after all the tests have run
        """
        super(BaseReportTest, cls).tearDownClass()
        cls.browser.quit()

    def setUp(self):
        """
        This function runs before each test case
        """
        pass

    def tearDown(self):
        """
        This function runs after each test case
        """
        pass

    @staticmethod
    def _clear_sessions():
        """
        Query and delete orphan sessions.
        """
        # get sessions in queue
        r = requests.get("{}/se/grid/newsessionqueue/queue".format(selenium_host))
        queued_sessions = json.loads(r.text)['value']

        # delete all sessions
        r = requests.get("{}/status".format(selenium_host))

        data = json.loads(r.text)
        for node in data['value']['nodes']:
            for slot in node['slots']:
                if slot['session']:
                    id = slot['session']['sessionId']
                    r = requests.delete("{}/session/{}".format(selenium_host, id))

        # recursively call to delete new sessions started from queue
        if len(queued_sessions) > 0:
            time.sleep(1)
            BaseReportTest._clear_sessions()

    @staticmethod
    def page_has_loaded(browser):
        page_state = browser.execute_script('return document.readyState;')
        return page_state == 'complete'

    def _navigate_to_dynamix_and_login(self):
        """
        Navigate to DynaMiX and log in.
        """
        self.browser.get(dynamix_url)

        # Fill in username
        self.browser.find_element_by_name("userName").send_keys(dynamix_user)

        # Fill in password
        self.browser.find_element_by_name("password").send_keys(dynamix_password)

        # Click on sign in
        btn_sign_in = self.browser.find_element_by_xpath("//*[@ng-class='buttonClass()']")
        btn_sign_in.click()

        # Wait for page to load
        WebDriverWait(self.browser, DEFAULT_TIMEOUT, 1).until(self.page_has_loaded)
        time.sleep(1)

    @staticmethod
    def get_downloaded_files(browser):
        """
        """
        if not browser.current_url.startswith("chrome://downloads"):
            browser.get("chrome://downloads/")

        files = browser.execute_script("""
            return document.querySelector('downloads-manager')
                .shadowRoot.querySelector('#downloadsList')
                .items.filter(e => e.state === 'COMPLETE')
                .map(e => e.filePath || e.file_path || e.fileUrl || e.file_url);
        """)
        return files

    def get_file_content(self, path):
        """
        """
        elem = self.browser.execute_script(
            "var input = window.document.createElement('INPUT'); "
            "input.setAttribute('type', 'file'); "
            "input.hidden = true; "
            "input.onchange = function (e) { e.stopPropagation() }; "
            "return window.document.documentElement.appendChild(input); ")

        elem._execute('sendKeysToElement', {'value': [path], 'text': path})

        result = self.browser.execute_async_script(
            "var input = arguments[0], callback = arguments[1]; "
            "var reader = new FileReader(); "
            "reader.onload = function (ev) { callback(reader.result) }; "
            "reader.onerror = function (ex) { callback(ex.message) }; "
            "reader.readAsDataURL(input.files[0]); "
            "input.remove(); ", elem)

        if not result.startswith('data:'):
            raise Exception("Failed to get file content: %s" % result)

        return base64.b64decode(result[result.find('base64,') + 7:])
