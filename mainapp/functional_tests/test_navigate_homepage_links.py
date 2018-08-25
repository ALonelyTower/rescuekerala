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
        expected_english_text = "Request For Help"
        expected_malayalam_text = "സഹായം അഭ്യർത്ഥിക്കാൻ"
        self.selenium.get(self.live_server_url)

        request_help_link = self.selenium.find_element_by_partial_link_text(expected_malayalam_text)
        request_help_link.click()
        actual_english_header = self.selenium.find_element_by_tag_name("h1").text
        actual_malayalam_header = self.selenium.find_element_by_tag_name("h2").text

        self.assertIn("/request/", self.selenium.current_url)
        self.assertIn(expected_english_text, actual_english_header)
        self.assertIn(expected_malayalam_text, actual_malayalam_header)
