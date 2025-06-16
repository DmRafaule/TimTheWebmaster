from selenium import webdriver
from selenium.webdriver.firefox.options import Options

import unittest

class NewVisitorTest(unittest.TestCase):
    """ Testing a new visitor """
    
    def setUp(self):
        firefox_opt = Options()
        firefox_opt.add_argument('--headless')
        firefox_opt.add_argument("--no-sandbox")
        firefox_opt.add_argument("--disable-dev-shm-usage")  
        self.browser = webdriver.Firefox(options=firefox_opt)
    
    def tearDown(self):
        self.browser.quit()
    
    def test_visit_home_page(self):
        #Visitor has entered the home page via search engine
        self.browser.get('http://localhost:8000')
        self.assertIn('Tim the Webmaster', self.browser.title)


if __name__ == "__main__":
    unittest.main(warnings='ignore')
