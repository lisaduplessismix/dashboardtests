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
from insights_dashboards.shared.base_dashboard_test_class import DEFAULT_TIMEOUT, BaseDashboardTest


# fetch config
dynamix_url = os.getenv('DYNAMIX_URL')


class TestDashboardExample(BaseDashboardTest):

    def test_kpi_widget_titles_english(self):
        """
        """
        # test_org_id = -1454670768671264798

        # navigate to dashboards
        self.navigate_to_dashboards(f"{dynamix_url}/#/insight/dashboards")

        # select org
        self.select_organisation("TODO")

        # switch to nested logi iframe
        self.switch_to_logi_iframe()

        # navigate to KPI goals page
        btn_kpi_goals = self.browser.find_element_by_id('btnKPIGoals')
        btn_kpi_goals.click()

        # to focus on a KPI widget we need to apply a few tricks to get to the correct iframe
        kpi_widget_titles = []
        WebDriverWait(self.browser, DEFAULT_TIMEOUT).until(EC.presence_of_element_located((By.TAG_NAME, "iframe")))
        elements = self.browser.find_elements(By.TAG_NAME, 'iframe')
        for element in elements:
            self.switch_to_logi_iframe()
            WebDriverWait(self.browser, 5).until(EC.frame_to_be_available_and_switch_to_it(element))
            e = WebDriverWait(self.browser, DEFAULT_TIMEOUT).until(EC.presence_of_element_located((By.ID, "divChartTitle")))
            title = e.find_element_by_tag_name("strong").text 
            kpi_widget_titles.append(title)

        # verify that all the widgets are there and have the correct titles
        assert 'KPI GOAL - EVENTS THAT AFFECT MY DRIVER SCORES' in kpi_widget_titles
        assert 'KPI GOAL - EVENTS THAT AFFECT MY ASSETS AND ASSOCIATED COSTS' in kpi_widget_titles
        assert 'THIS IS A PERFORMANCE CHART, NOT AN EVENT CHART' in kpi_widget_titles
