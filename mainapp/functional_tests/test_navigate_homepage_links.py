from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver


class HomePageHyperLinksTest(StaticLiveServerTestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.selenium = webdriver.Firefox()
        cls.selenium.implicitly_wait(10)

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super().tearDownClass()

    def test_navigate_from_home_to_requestforhelp(self):
        homepage_requesthelp_link_text = "Request\nfor help\nസഹായം അഭ്യര്‍ഥിക്കാന്‍" 
        requestpage_header_english_text = "Request For Help"
        requestpage_header_malayalam_text = "സഹായം അഭ്യര്‍ഥിക്കാന്‍"

        self.selenium.get(self.live_server_url)
        request_help_link = self.selenium.find_element_by_link_text(homepage_requesthelp_link_text)
        request_help_link.click()

        self.assertIn("/request/", self.selenium.current_url)
        self.assertIn(requestpage_header_english_text, self.selenium.page_source)
        self.assertIn(requestpage_header_malayalam_text, self.selenium.page_source)