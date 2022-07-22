from bs4.element import PageElement
from typing import Dict, Callable
from pprint import pprint
from utils import make_soup
from markdownify import markdownify, MarkdownConverter


# Create shorthand method for conversion
def md(soup, **options):
    return MarkdownConverter(**options).convert_soup(soup)


class Beacon:
    def __init__(self, beacon: PageElement):
        self._beacon: PageElement = beacon
        self._job_post: Dict[str, str] = {}
        self.populate_from_job_card()
        self.populate_from_iframe()
        pprint(self._job_post)

    @property
    def dict(self):
        return self._job_post

    def populate_from_job_card(self):
        # self.make_attribute('title', lambda: self._beacon.find_next('a', class_='jcs-JobTitle').text)

        title = self._beacon.find('a', class_='jcs-JobTitle')
        self._job_post['title'] = title.text
        self._job_post['url'] = f"https://www.indeed.com{title['href']}"
        company_name = self._beacon.find('span', class_='companyName').text
        self._job_post['company_name'] = company_name

        self.make_attribute('company_rating',
                            lambda: self._beacon.find('span', class_='ratingNumber').find('span').text)

        company_location = self._beacon.find('div', class_='companyLocation').text
        self._job_post['company_location'] = company_location

        self.make_attribute('estimated_salary',
                            lambda: self._beacon.find('span', class_='estimated-salary').find('span').text)

        self.make_attribute('salary',
                            lambda: self._beacon.find('div', class_='salary-snippet-container').find('div',
                                                                                                     class_='attribute_snippet').text)

        self.make_attribute('job_type', lambda:
        self._beacon.find('div', class_='salaryOnly').find_all('div', class_='metadata')[1].text)
        self.make_attribute('multiple_candidates',
                            lambda: self._beacon.find('table', class_='jobCardShelfContainer').find('td',
                                                                                                    class_='hiringMultipleCandidates').text)
        self.make_attribute('date_posted',
                            lambda: self._beacon.find('table', class_='jobCardShelfContainer').find('span',
                                                                                                    class_='date').text.replace(
                                'Posted', ''))

    def make_attribute(self, name: str, command: Callable):
        """
        Creates an optional attribute on the self._job_post dict
        and catches if the classname was not found by BeautifulSoap
        :param name: attribute name
        :param command: labda function as a command to extract attribute from a beacon:PageElement
        :return: None
        example usage: self.make_attribute('title', lambda: self._beacon.find_next('a', class_='jcs-JobTitle').text)
        """
        attribute_value = None
        try:
            attribute_value = command()
        except Exception as e:
            print(f'Error finding {name} for job {self._job_post["title"]}', e)
        self._job_post[name] = attribute_value

    def populate_from_iframe(self):
        url = self._job_post['url']
        soup = make_soup(url, f'{self._job_post["title"]}-{self._job_post["company_name"]}.html')
        self.make_attribute('qualifications',
                            lambda: ', '.join(li.text for li in
                                              soup.select_one('#qualificationsSection')
                                              .find('ul')
                                              .find_all('li'))
                            )

        self.make_attribute('benefits',
                            lambda: ', '.join(div.text for div in
                                              soup.select_one('#benefits').find_all('div', class_='ecydgvn1'))
                            )  # TODO test for multiple benefits

        self.make_attribute('description_markdown',
                            lambda: markdownify(str(soup.select_one('#jobDescriptionText')))
                            )
        self.make_attribute('description_text',
                            lambda: soup.select_one('#jobDescriptionText').get_text()
                            )
        self.make_attribute('company_indeed_profile_url',
                            lambda: soup.find('div', class_='jobsearch-JobInfoHeader-subtitle').find('a')['href']
                            )
        self.make_attribute('hiring_insights',
                            lambda: ", ".join(
                                p.text for p in soup.select_one('#hiringInsightsSectionRoot').find_all('p'))
                            )
