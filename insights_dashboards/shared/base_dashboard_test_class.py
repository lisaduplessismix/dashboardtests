import os
import time
import json
import base64
import requests
import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


# import configuration
selenium_host = os.getenv('SELENIUM_HOST')
webdriver_url = f"{selenium_host}/wd/hub"
dynamix_url = os.getenv('DYNAMIX_URL')
dynamix_user = os.getenv('DYNAMIX_USER')
dynamix_password = os.getenv('DYNAMIX_PASSWORD')

DEFAULT_TIMEOUT = 60


class BaseDashboardTest(unittest.TestCase):

    def __init__(self, methodName: str = ...) -> None:
        super().__init__(methodName)

    @classmethod
    def setUpClass(cls):
        """
        This function runs once before any of the tests in the class runs
        """
        super(BaseDashboardTest, cls).setUpClass()
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
        super(BaseDashboardTest, cls).tearDownClass()
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
            BaseDashboardTest._clear_sessions()

    @staticmethod
    def page_has_loaded(browser):
        page_state = browser.execute_script('return document.readyState;')
        return page_state == 'complete'

    def navigate_to_dashboards(self, url):
        """
        Navigate to a url in a more robust way.
        """
        time.sleep(2)
        self.browser.get(url)
        WebDriverWait(self.browser, DEFAULT_TIMEOUT).until(EC.presence_of_element_located((By.XPATH, "//span[text() = 'Dashboards']")))

    def _navigate_to_dynamix_and_login(self):
        """
        Navigate to DynaMiX and log in.
        """
        self.browser.get(dynamix_url)
        WebDriverWait(self.browser, DEFAULT_TIMEOUT).until(EC.presence_of_element_located((By.XPATH, "//*[@ng-class='buttonClass()']")))

        # Fill in username
        self.browser.find_element_by_name("userName").send_keys(dynamix_user)

        # Fill in password
        self.browser.find_element_by_name("password").send_keys(dynamix_password)

        # Click on sign in
        btn_sign_in = self.browser.find_element_by_xpath("//*[@ng-class='buttonClass()']")
        btn_sign_in.click()
        time.sleep(3)  # allow site to redirect

        # Wait for page to load
        WebDriverWait(self.browser, DEFAULT_TIMEOUT).until(EC.presence_of_element_located((By.XPATH, "//div[contains(@class, 'brand')]")))

    def select_organisation(self, org_name):
        """
        Select a given organisation
        """
        print("#TODO..")

    def switch_to_logi_iframe(self):
        """
        Switch to the embedded iframe that Logi runs in
        """
        i = 0
        while True:
            i += 1
            if i == 30:
                raise Exception("Could not switch to Logi iframe")
            try:
                self.browser.switch_to.default_content()

                # switch to 1st iframe
                WebDriverWait(self.browser, 5).until(EC.frame_to_be_available_and_switch_to_it((By.ID, "frameHostAdapter")))

                # switch to 2nd iframe (There is a redirect on this frame so we need to wait for the correct one to be loaded)
                WebDriverWait(self.browser, 5).until(EC.frame_to_be_available_and_switch_to_it((By.XPATH, "//iframe[starts-with(@id, 'rdFrame')]")))
                WebDriverWait(self.browser, 5).until(EC.presence_of_element_located((By.ID, 'btnKPIGoals')))
                break
            except:
                time.sleep(1)
