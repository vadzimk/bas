import re

from bs4 import BeautifulSoup
from bs4.element import PageElement
from pprint import pprint

from BaseBeacon import BaseBeacon
from utils import make_soup, override, save_safe
from markdownify import markdownify, MarkdownConverter


# Create shorthand method for conversion
def md(soup, **options):
    return MarkdownConverter(**options).convert_soup(soup)


class LinkedinBeacon(BaseBeacon):
    def __init__(self, beacon: PageElement):
        super().__init__(beacon)
        self.populate_from_job_card()

        self._job_post = {k: (" ".join(v.strip().replace('\n\n', ',').split()) if type(v) == str else v) for k, v in
                          self._job_post.items()}

    @property
    def dict(self):
        return self._job_post

    @override
    def populate_from_job_card(self):
        # self.make_attribute('title', lambda: self._beacon.find_next('a', class_='jcs-JobTitle').text)

        title = self._beacon.find('a', class_='job-card-list__title')

        self.make_attribute('title', lambda: title.text)

        self.make_attribute('url', lambda: f"https://www.linkedin.com{title['href']}")

        self.make_attribute('company_name',
                            lambda: self._beacon.find('a', class_='job-card-container__company-name').text)

        self.make_attribute('company_rating',
                            lambda: None)

        self.make_attribute('company_location',
                            lambda: self._beacon.find('div', class_='artdeco-entity-lockup__caption').text)

        self.make_attribute('date_posted',
                            lambda: self._beacon.find('li', class_='job-card-container__listed-time').text)

        # self.make_attribute('number_of_applicants',
        #                     lambda: self._beacon.find('span', class_='jobs-unified-top-card__applicant-count').text)

    @override
    def populate_from_details(self, job_view_html):
        save_safe(job_view_html, f'{self._job_post["title"]}-{self._job_post["company_name"]}.html')
        # -----------------
        # Continue from here
        soup = BeautifulSoup(job_view_html, 'html.parser')

        # self.make_attribute('qualifications',
        #                     lambda: ', '.join(li.text for li in
        #                                       soup.select_one('#qualificationsSection')
        #                                       .find('ul')
        #                                       .find_all('li')))

        self.make_attribute('benefits',
                            lambda: ', '.join(div.text for div in
                                              soup.find_all('.featured-benefits__benefit-list'))
                            )  # TODO test for multiple benefits

        self.make_attribute('description_markdown',
                            lambda: markdownify(str(soup.select_one('#job-details')))
                            )
        self.make_attribute('description_text',
                            lambda: soup.select_one('#job-details').get_text().strip()
                            )
        self.make_attribute('company_profile_url',
                            lambda: re.sub(r"life/$", "",
                                           f"https://www.linkedin.com{soup.find('span', class_='jobs-unified-top-card__company-name').find('a')['href']}")
                            )

        # self.make_attribute('hiring_insights',
        #                     lambda: ", ".join(
        #                         p.text for p in soup.select_one('#hiringInsightsSectionRoot').find_all('p')))

        # TODO from full description
        # self.make_attribute('estimated_salary',
        #                     lambda: self._beacon.find('span', class_='estimated-salary').find('span').text)

        # TODO from full description
        # self.make_attribute('salary',
        #                     lambda: self._beacon.find('div', class_='salary-snippet-container').find('div',
        #                                                                                              class_='attribute_snippet').text)

        # TODO from full description
        # self.make_attribute('job_type', lambda:
        # self._beacon.find('div', class_='salaryOnly').find_all('div', class_='metadata')[1].text)



    def populate_from_company_profile(self, about_company_html, about_employees_html):
        save_safe(about_company_html, f"{self._job_post['company_name']}.html")
        save_safe(about_employees_html, f"{self._job_post['company_name']}--employees.html")
        company_soup = BeautifulSoup(about_company_html, 'html.parser')


        self.make_attribute("company_overview",
                            lambda: company_soup.find('h2', string=re.compile(".*Overview.*")).find_next('p').text)

        self.make_attribute('company_homepage',
                            lambda: company_soup.find('span', class_="link-without-visited-state").text.strip())

        self.make_attribute('company_industry',
                            lambda: company_soup.find('dt', string=re.compile(".*Industry.*")).find_next('dd').text.strip())

        self.make_attribute('company_size',
                            lambda: company_soup.find('dt', string=re.compile(".*Company size.*"))
                            .find_next('dd').text.replace(' employees', '').strip())

        # find number of employess on linkedin from the employees section
        # self.make_attribute('company_employees_on_linkedin',
        #                     lambda: company_soup.find('dt', string=re.compile(".*Company size.*"))
        #                     .find_next('dd').find_next('dd').text.replace(' on LinkedIn', ''))

        employee_soup = BeautifulSoup(about_employees_html, 'html.parser')

        self.make_attribute("number_employees",
                            lambda: re.search(r'\d+',
                                              employee_soup.find('span',
                                                                 string=re.compile(".*employees.*")).text).group())

        country_buttons = employee_soup \
            .find('div', class_='insight-container') \
            .find_all('button', class_='org-people-bar-graph-element--is-selectable')

        self.make_attribute(
            'main_country_number_employees', lambda: country_buttons[0].find('strong').text)

        self.make_attribute('main_country_name',
                            lambda: country_buttons[0].find('span', class_='org-people-bar-graph-element__category').text)

        self.make_attribute('other_locations_employees',
                            lambda: ", ".join([b.text.strip() for b in country_buttons[1:]]))

