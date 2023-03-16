import re

from bs4 import BeautifulSoup
from bs4.element import PageElement
from pprint import pprint

from BaseBrowserBeacon import BaseBrowserBeacon

from utils import override, make_soup, save_safe, replace_p_br_p, age_to_date
from markdownify import markdownify, MarkdownConverter


# Create shorthand method for conversion
def md(soup, **options):
    return MarkdownConverter(**options).convert_soup(soup)


class IndeedBeacon(BaseBrowserBeacon):
    def __init__(self, beacon: PageElement):
        super().__init__(beacon)
        self.populate_from_job_card()
        # pprint(self._job_post)

    @property
    def dict(self):
        return self._job_post

    @staticmethod
    def extract_job_url_from_url(s):
        prefix = 'https://www.indeed.com/viewjob?jk='
        suffix = re.split(r'=|&', s)[1]
        if suffix == 'r':
            pass
        else:
            s = prefix + suffix
        return s

    def populate_from_job_card(self):
        # self.make_attribute('title', lambda: self._beacon.find_next('a', class_='jcs-JobTitle').text)

        title = self._beacon.find('a', class_='jcs-JobTitle')
        self.make_attribute('title', lambda: title.text)
        self.make_attribute('url', lambda: self.extract_job_url_from_url(f"https://www.indeed.com{title['href']}"))
        self.make_company_attribute('name', lambda: self._beacon.find('span', class_='companyName').text)

        self.make_company_attribute('rating',
                                    lambda: self._beacon.find('span', class_='ratingNumber').find('span').text)

        self.make_company_attribute('location', lambda: self._beacon.find('div', class_='companyLocation').text)

        self.make_attribute('estimated_salary',
                            lambda: self._beacon.find('span', class_='estimated-salary').find('span').text.replace(
                                'Estimated', ''))

        self.make_attribute('salary',
                            lambda: self._beacon.find('div', class_='salary-snippet-container').find('div',
                                                                                                     class_='attribute_snippet').text)

        self.make_attribute('job_type',
                            lambda: self._beacon.find('div', class_='salaryOnly').find_all('div', class_='metadata')[
                                1].text)
        self.make_attribute('multiple_candidates',
                            lambda: self._beacon.find('table', class_='jobCardShelfContainer').find('td',
                                                                                                    class_='hiringMultipleCandidates').text)

        self.make_attribute('created_str',
                            lambda: self._beacon
                            .find('table', class_='jobCardShelfContainer')
                            .find('span', class_='date')
                            .text.replace('Posted', ''))
        self.make_attribute('date_posted',
                            lambda: age_to_date(self._job_post['created_str']))

    def populate_from_details(self, job_view_html):
        # save_safe(job_view_html, f'{self._job_post["title"]}-{self._job_post["company"]["name"]}.html')
        soup = BeautifulSoup(job_view_html, 'html.parser')
        self.make_attribute('qualifications',
                            lambda: ', '.join(li.text for li in
                                              soup.select_one('#qualificationsSection')
                                              .find('ul')
                                              .find_all('li')))

        self.make_attribute('benefits',
                            lambda: ', '.join(div.text for div in
                                              soup.select_one('#benefits').find_all('div', class_='ecydgvn1'))
                            )  # TODO test for multiple benefits

        self.make_attribute('description_markdown',
                            lambda: markdownify(str(soup.select_one('#jobDescriptionText'))))

        self.make_attribute('description_text',
                            lambda: soup.select_one('#jobDescriptionText').get_text())

        if not self._job_post.get('description_text'):
            message = f'[description_text] empty on page: {self._job_post["url"]}'
            raise RuntimeError(message)

        self.make_attribute('description_html',
                            lambda: replace_p_br_p(str(soup.select_one('#jobDescriptionText'))))

        self.make_company_attribute('profile_url',
                                    # lambda:  # outdated selector
                                    # soup.find('div', class_='jobsearch-JobInfoHeader-subtitle').find('a')['href'].split(
                                    #     '?')[0],
                                    lambda:  # new selector
                                    soup.find('div', class_='jobsearch-CompanyInfoContainer').find('a')['href'].split(
                                        '?')[0],
                                    )
        self.make_attribute('hiring_insights',
                            lambda: ", ".join(
                                re.sub('Posted.*ago', '', p.text) for p in soup.select_one('#hiringInsightsSectionRoot').find_all('p'))
                            )

        self.make_attribute('original_url',
                                    lambda:
                                    soup.find(id='originalJobLinkContainer').find('a')['href'],
                                    )

    @override
    def populate_from_company_profile(self, about_company_html, about_employees_html=None):
        """ all must be company fields """
        # save_safe(about_company_html, f"{self._job_post['company']['name']}.html")
        company_soup = BeautifulSoup(about_company_html, 'html.parser')

        self.make_company_attribute("overview",
                                    lambda: company_soup.find('div',
                                                              attrs={"data-tn-section": "AboutSection-section"})
                                    .find('section')
                                    .find_all('div', recursive=False)[2].text.replace('Learn more', '---'))

        self.make_company_attribute('homepage_url',
                                    lambda: company_soup.find(attrs={"data-testid": "companyInfo-companyWebsite"})
                                    .find_all('div')[1].find('a')['href'])

        self.make_company_attribute('industry',
                                    lambda: company_soup.find(attrs={"data-testid": "companyInfo-industry"})
                                    .find_all('div')[1].text)

        self.make_company_attribute('size',
                                    lambda: BaseBrowserBeacon.company_size_map
                                    .get(company_soup.find(attrs={"data-testid": "companyInfo-employee"})
                                    .find_all('div')[1].text))

        self.make_company_attribute('other_locations_employees',
                                    lambda: company_soup.find(attrs={"data-testid": "companyInfo-headquartersLocation"})
                                    .find_all('div')[1].text)

        self.make_company_attribute('other_locations_employees_html',
                                    lambda: "<ul><li>" +
                                            company_soup.find(attrs={"data-testid": "companyInfo-headquartersLocation"})
                                    .find_all('div')[1].text.strip() + "</li></ul>")
