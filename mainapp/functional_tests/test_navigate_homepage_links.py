from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.webdriver import FirefoxOptions


class HomePageHyperLinksTest(StaticLiveServerTestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        opts = FirefoxOptions()
        opts.add_argument("--headless")
        cls.selenium = webdriver.Firefox(firefox_options=opts)
        cls.selenium.implicitly_wait(10)

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super().tearDownClass()

    def test_navigate_from_home_to_requestforhelp(self):
        requesthelp_link_malayalam_text = "സഹായം അഭ്യര്‍ഥിക്കാന്‍"
        requestpage_header_english_text = "Request For Help"

        self.selenium.get(self.live_server_url)
        request_help_link = self.selenium.find_element_by_partial_link_text(requesthelp_link_malayalam_text)
        request_help_link.click()

        self.assertIn("/request/", self.selenium.current_url)
        self.assertIn(requestpage_header_english_text, self.selenium.page_source)
        self.assertIn(requesthelp_link_malayalam_text, self.selenium.page_source)