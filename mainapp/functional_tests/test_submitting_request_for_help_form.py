from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver import FirefoxOptions
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from unittest.mock import patch
from mainapp.views import CreateRequest
from django.http import HttpResponseRedirect


class RequestHelpFormSubmissionTest(LiveServerTestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        opts = FirefoxOptions()
        opts.add_argument("--headless")
        cls.selenium = webdriver.Firefox(firefox_options=opts)
        cls.selenium.implicitly_wait(5)

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super().tearDownClass()

    def fake_form_valid(self, form):
        """
        A mock method for replacing form_valid in mainapp.views.CreateRequest
        The commit is set to false; otherwise, there's a race condition between
            the commit and the destruction of the database.
        """
        self.object = form.save(commit=False)
        return HttpResponseRedirect(self.get_success_url())

    @patch.object(CreateRequest, 'form_valid', fake_form_valid)
    def test_submitting_request_for_help_form(self):
        # Go to homepage of kelararescue
        self.selenium.get(self.live_server_url)

        # Click on Request for Help link
        self.selenium.find_element_by_partial_link_text("സഹായം അഭ്യർത്ഥിക്കാൻ").click()

        # Check if we're on the requests page
        self.assertIn('/request/', self.selenium.current_url)

        self._click_ok_in_allow_location_window()

        self._fill_out_request_help_form()

        # Submit form
        request_form = self.selenium.find_element_by_tag_name("form")
        request_form.find_element_by_tag_name("button").click()

        # Check if we're on the request success page
        self.assertIn("/req_sucess/", self.selenium.current_url)


    def _fill_out_request_help_form(self):
        # Click to open dropdown window
        self.selenium.find_element_by_class_name("selectize-control").click()

        # Select District from dropdown
        district_dropdown_content = self.selenium.find_element_by_class_name("selectize-dropdown-content")
        allapuzha_option = district_dropdown_content.find_element_by_css_selector("div.option")
        allapuzha_option.click()

        location_textbox = self.selenium.find_element_by_id("id_location")
        location_textbox.send_keys("United States")

        requestee_textbox = self.selenium.find_element_by_id("id_requestee")
        requestee_textbox.send_keys("John Smith")

        requestee_phone_textbox = self.selenium.find_element_by_id("id_requestee_phone")
        requestee_phone_textbox.send_keys("5555555555")

        # Check off all Need checkboxes
        self.selenium.find_element_by_id("id_is_request_for_others").click() 
        self.selenium.find_element_by_id("id_needrescue").click() 
        self.selenium.find_element_by_id("id_needwater").click() 
        self.selenium.find_element_by_id("id_needfood").click() 
        self.selenium.find_element_by_id("id_needcloth").click() 
        self.selenium.find_element_by_id("id_needmed").click() 
        self.selenium.find_element_by_id("id_needkit_util").click() 
        self.selenium.find_element_by_id("id_needtoilet").click() 

        other_needs_textbox = self.selenium.find_element_by_id("id_needothers")
        other_needs_textbox.send_keys("Blankets and Towels")

        manual_location_textbox = self.selenium.find_element_by_id("pac-input")
        manual_location_textbox.send_keys("Palazhi Rd, Karamuck, Manalur, Kerala 680617, India")

    def _click_ok_in_allow_location_window(self):
        """
        Important to deal with this window as it prevents interaction with some elements of the form.
        """
        MAX_WAIT = 5
        wait = WebDriverWait(self.selenium, MAX_WAIT)

        # Wait until Allow Location window appears
        wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "modal-dialog")))

        # Scroll to Allow Location 'OK' button, then click to close
        modal_dialog_window = self.selenium.find_element_by_class_name("modal-dialog")
        actions = ActionChains(self.selenium)
        actions.move_to_element(modal_dialog_window).perform()
        self.selenium.find_element_by_id("modal_ok_button").click()

        # Wait until the Allow Location window fades
        wait.until(EC.invisibility_of_element_located((By.CLASS_NAME, "modal-backdrop")))


