# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
import unittest, time, re

class FoSeleniumRecorded(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Firefox()
        self.driver.implicitly_wait(30)
        self.base_url = "http://www.footballoutsiders.com/"
        self.verificationErrors = []
        self.accept_next_alert = True
    
    def test_fo_selenium_recorded(self):
        driver = self.driver
        driver.get(self.base_url + "/")
        driver.find_element_by_id("edit-name").clear()
        driver.find_element_by_id("edit-name").send_keys("eric.truett@gmail.com")
        driver.find_element_by_id("edit-pass").clear()
        driver.find_element_by_id("edit-pass").send_keys("cft0911")
        driver.find_element_by_id("edit-submit").click()
        driver.find_element_by_css_selector("img[alt=\"My FO Downloads\"]").click()
        driver.find_element_by_xpath("(//a[contains(text(),'download')])[4]").click()
    
    def is_element_present(self, how, what):
        try: self.driver.find_element(by=how, value=what)
        except NoSuchElementException, e: return False
        return True
    
    def is_alert_present(self):
        try: self.driver.switch_to_alert()
        except NoAlertPresentException, e: return False
        return True
    
    def close_alert_and_get_its_text(self):
        try:
            alert = self.driver.switch_to_alert()
            alert_text = alert.text
            if self.accept_next_alert:
                alert.accept()
            else:
                alert.dismiss()
            return alert_text
        finally: self.accept_next_alert = True
    
    def tearDown(self):
        self.driver.quit()
        self.assertEqual([], self.verificationErrors)

if __name__ == "__main__":
    unittest.main()
