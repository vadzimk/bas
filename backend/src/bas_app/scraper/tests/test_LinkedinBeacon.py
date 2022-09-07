import unittest

from bs4 import BeautifulSoup

from ..LinkedinBeacon import LinkedinBeacon

class TestLinkedinBeacon(unittest.TestCase):
    def test_populate_from_job_card_company_name(self):
        """ can find company name attribute"""
        s = """<div id="ember42" class="artdeco-entity-lockup__subtitle ember-view">
          <span class="job-card-container__primary-description ">
            <a class="app-aware-link" target="_self" href="https://www.linkedin.com/company/edward-jones/"><!---->Edward Jones<!----></a>
          </span>

      </div>"""
        soup = BeautifulSoup(s, 'html.parser')
        beacon = LinkedinBeacon(soup)
        beacon.populate_from_job_card()
        print(beacon.dict)

        self.assertIn('name', beacon.dict['company'])

if __name__ == '__main__':
    unittest.main()