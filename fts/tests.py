from django.test import LiveServerTestCase
from selenium import webdriver

class NavigateTestCase(LiveServerTestCase):
    
    def setUp(self):
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(3)

    def tearDown(self):
        self.browser.quit()

    def _navigate_to_homepage(self):
        self.browser.get(self.live_server_url)
        body = self.browser.find_element_by_tag_name('body')
        return body
    
class GigTest(NavigateTestCase):
   
    def test_post_a_job(self):
        #navigate to post_job
        body = self.browser.get(self.live_server_url + '/post_job')
        #user fill out the form and preview it
        body = self.browser.find_element_by_tag_name('body')
        self.assertIn('Create Your Job Listing', body.text)
        # select a job type
        #type_chosen = self.browser.find_element_by_css_selector(
        #    "input[value='1']"
        #)
        #type_chosen.click()
        # select a job category
        category_chosen = self.browser.find_elements_by_css_selector(
            "option[value='1']"
        )
        category_chosen.click()
        # fill out the title
        title = self.browser.find_element_by_id("id_title")

