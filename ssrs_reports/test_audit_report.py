import os
import json
import requests
import unittest
import sys
import time
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from ssrs_reports.shared.base_report_test_class import DEFAULT_TIMEOUT, BaseReportTest


# fetch config
dynamix_url = os.getenv('DYNAMIX_URL')


class TestAuditReports(BaseReportTest):

    def test_config_audit_report(self):
        """
        """
        test_org_id = -1454670768671264798

        # navigate to report
        self.browser.get(f"{dynamix_url}/#/insight/reports/setup?orgId={test_org_id}&path=%2FFM%2FAudit%20Reports%2FConfig%20Audit%20Report")

        # wait for page to load
        WebDriverWait(self.browser, DEFAULT_TIMEOUT).until(EC.presence_of_element_located((By.XPATH, '//span[contains(text(),"Report on")]')))

        # search
        self.browser.find_element_by_css_selector(".filter-search-input").send_keys("Ford")

        # select filtered element
        WebDriverWait(self.browser, DEFAULT_TIMEOUT).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'td.selection')))
        row_to_select = self.browser.find_element_by_css_selector('td.selection')
        row_to_select.click()

        # click next
        self.browser.find_element_by_xpath("//BUTTON[@class='btn-wide btn-small btn-success btn ng-scope ng-binding'][text()='Next']").click()

        # wait for page to load
        WebDriverWait(self.browser, DEFAULT_TIMEOUT).until(EC.presence_of_element_located((By.XPATH, '//h5[contains(text(),"Select report period")]')))

        # choose period
        drop_down = Select(self.browser.find_element_by_css_selector("select.span3"))
        drop_down.select_by_visible_text("Rolling 12 Months")

        # click next
        self.browser.find_element_by_xpath("//BUTTON[@class='btn-wide btn-small btn-success btn ng-scope ng-binding'][text()='Next']").click()

        # choose to download the report
        WebDriverWait(self.browser, DEFAULT_TIMEOUT).until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.form-inline:nth-child(2) > select:nth-child(2)")))
        drop_down = Select(self.browser.find_element_by_css_selector("div.form-inline:nth-child(2) > select:nth-child(2)"))
        drop_down.select_by_visible_text("Download")

        # click on run
        self.browser.find_element_by_xpath("//BUTTON[@class='btn-wide btn-small btn-success btn ng-scope ng-binding'][text()='Run']").click()

        # list all the completed remote files (waits for at least one)
        files = WebDriverWait(self.browser, DEFAULT_TIMEOUT, 1).until(self.get_downloaded_files)

        # get the content of the first file remotely
        content = self.get_file_content(files[0])

        # save the content in a local file in the working directory
        report_path = os.path.join(self.downloaded_reports_folder, os.path.basename(files[0]))
        with open(report_path, 'wb') as f:
            f.write(content)

        # validate that the report has been created
        assert os.path.isfile(report_path)

    def test_satellite_status_and_audit_report(self):
        """
        """
        test_org_id = 8308618011429325423

        # navigate to report
        self.browser.get(f"{dynamix_url}/#/insight/reports/setup?orgId={test_org_id}&path=%2FFM%2FAudit%20Reports%2FSatellite%20Status%20and%20Audit%20Report")

        # wait for page to load
        WebDriverWait(self.browser, DEFAULT_TIMEOUT).until(EC.presence_of_element_located((By.XPATH, '//span[contains(text(),"Report on")]')))

        # search
        row_to_select = self.browser.find_element_by_css_selector(
            "span.report-parameter:nth-child(9) > span:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > input:nth-child(1)")
        row_to_select.send_keys("300234062202870")

        # select filtered element
        WebDriverWait(self.browser, DEFAULT_TIMEOUT).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'td.selection')))
        row_to_select = self.browser.find_element_by_css_selector('td.selection')
        row_to_select.click()

        # click next
        self.browser.find_element_by_xpath("//BUTTON[@class='btn-wide btn-small btn-success btn ng-scope ng-binding'][text()='Next']").click()

        # wait for page to load
        WebDriverWait(self.browser, DEFAULT_TIMEOUT).until(EC.presence_of_element_located((By.XPATH, '//h5[contains(text(),"Select report period")]')))

        # choose period
        drop_down = Select(self.browser.find_element_by_css_selector("select.span3"))
        drop_down.select_by_visible_text("Rolling 12 Months")

        # click next
        self.browser.find_element_by_xpath("//BUTTON[@class='btn-wide btn-small btn-success btn ng-scope ng-binding'][text()='Next']").click()

        # choose to download the report
        WebDriverWait(self.browser, DEFAULT_TIMEOUT).until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.form-inline:nth-child(2) > select:nth-child(2)")))
        drop_down = Select(self.browser.find_element_by_css_selector("div.form-inline:nth-child(2) > select:nth-child(2)"))
        drop_down.select_by_visible_text("Download")

        # click on run
        self.browser.find_element_by_xpath("//BUTTON[@class='btn-wide btn-small btn-success btn ng-scope ng-binding'][text()='Run']").click()

        # list all the completed remote files (waits for at least one)
        files = WebDriverWait(self.browser, DEFAULT_TIMEOUT, 1).until(self.get_downloaded_files)

        # get the content of the first file remotely
        content = self.get_file_content(files[0])

        # save the content in a local file in the working directory
        report_path = os.path.join(self.downloaded_reports_folder, os.path.basename(files[0]))
        with open(report_path, 'wb') as f:
            f.write(content)

        # validate that the report has been created
        assert os.path.isfile(report_path)

    def test_vehicle_road_speed_vs_gps_velocity_report(self):
        """
        """
        test_org_id = -1454670768671264798

        # navigate to report
        self.browser.get(f"{dynamix_url}/#/insight/reports/setup?orgId={test_org_id}&path=%2FFM%2FAudit%20Reports%2FVehicle%20Road%20Speed%20vs%20GPS%20Velocity%20Report")

        # wait for page to load
        WebDriverWait(self.browser, DEFAULT_TIMEOUT).until(EC.presence_of_element_located((By.XPATH, '//span[contains(text(),"Report on")]')))

        # checkboxes
        item_to_select = WebDriverWait(self.browser, DEFAULT_TIMEOUT).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".first-item > div:nth-child(2) > div:nth-child(1) > div:nth-child(2)")))
        item_to_select.click()

        # click next
        self.browser.find_element_by_xpath("//BUTTON[@class='btn-wide btn-small btn-success btn ng-scope ng-binding'][text()='Next']").click()
        WebDriverWait(self.browser, DEFAULT_TIMEOUT).until(EC.presence_of_element_located((By.XPATH, '//span[contains(text(),"Show Speed Difference Greater Than")]')))

        # click next
        self.browser.find_element_by_xpath("//BUTTON[@class='btn-wide btn-small btn-success btn ng-scope ng-binding'][text()='Next']").click()

        # wait for page to load
        # WebDriverWait(self.browser, DEFAULT_TIMEOUT).until(EC.presence_of_element_located((By.XPATH, '//h5[contains(text(),"Process report")]')))
        WebDriverWait(self.browser, DEFAULT_TIMEOUT).until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.form-inline:nth-child(2) > select")))

        # choose to download the report
        drop_down = Select(self.browser.find_element_by_css_selector("div.form-inline:nth-child(2) > select:nth-child(2)"))
        drop_down.select_by_visible_text("Download")

        # choose excel format
        drop_down = Select(self.browser.find_element_by_css_selector(
            "span.report-parameter:nth-child(4) > span:nth-child(1) > div:nth-child(1) > div:nth-child(2) > select:nth-child(2)"))
        drop_down.select_by_visible_text("EXCEL")

        # click on run
        self.browser.find_element_by_xpath("//BUTTON[@class='btn-wide btn-small btn-success btn ng-scope ng-binding'][text()='Run']").click()

        # list all the completed remote files (waits for at least one)
        files = WebDriverWait(self.browser, DEFAULT_TIMEOUT, 1).until(self.get_downloaded_files)

        # get the content of the first file remotely
        content = self.get_file_content(files[0])

        # save the content in a local file in the working directory
        report_path = os.path.join(self.downloaded_reports_folder, os.path.basename(files[0]))
        with open(report_path, 'wb') as f:
            f.write(content)

        # validate that the report has been created
        assert os.path.isfile(report_path)
