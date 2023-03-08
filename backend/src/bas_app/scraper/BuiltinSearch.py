import sys

from bas_app import db
from bas_app.models import Search, Company
from bas_app.scraper.BaseSearch import BaseSearch
import logging
import time
from dataclasses import dataclass
import requests
from urllib.parse import unquote
from bas_app.scraper.BuiltinBeacon import BuiltinBeacon
from bas_app.scraper.utils import override


@dataclass
class RequestFields:
    path: str
    params: dict
    headers: dict

    def __post_init__(self):
        self.host: str = "api.builtin.com"
        self.url = f"https://{self.host}{self.path}"


JOB_CATEGORIES = [
    {"id": 147, "name": "Data + Analytics", },
    {"id": 148, "name": "Design + UX", },
    {"id": 149, "name": "Developer + Engineer", },
    {"id": 146, "name": "Finance", },
    {"id": 150, "name": "HR", },
    {"id": 151, "name": "Internships", },
    {"id": 152, "name": "Legal", },
    {"id": 153, "name": "Marketing", },
    {"id": 154, "name": "Operations", },
    {"id": 155, "name": "Product", },
    {"id": 156, "name": "Project Mgmt", },
    {"id": 157, "name": "Sales", },
    {"id": 158, "name": "Content",
     }
]


class BuiltinSearch(BaseSearch):
    def __init__(self, *, what, where, job_category: list, limit, user_id: int = None,
                 search_model_id: int = None,
                 task_id: str = None):
        super().__init__(user_id=user_id, search_model_id=search_model_id, task_id=task_id)
        self._what = what  # TODO not used
        self._where = where  # TODO not used
        self._limit: int = int(limit) if limit else sys.maxsize
        self._job_category = job_category
        self._search_path = "/services/job-retrieval/legacy-collapsed-jobs"
        self._search_headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:109.0) Gecko/20100101 Firefox/109.0",
            "Accept": "*/*",
            "Accept-Language": "en,en-US;q=0.5",
            "Referer": "https://www.builtinla.com/",
            "Content-Type": "application/json",
            "Origin": "https://www.builtinla.com",
            "DNT": "1",
            "Connection": "keep-alive",
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "cross-site",
            "Sec-GPC": "1",
            "Pragma": "no-cache",
            "Cache-Control": "no-cache",
            "TE": "trailers"
        }
        self._company_base_path = "/companies/alias/"
        self._company_headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:109.0) Gecko/20100101 Firefox/109.0",
            "Accept": "application/json, text/plain, */*",
            "Accept-Language": "en,en-US;q=0.5",
            # "builtin-vue-version": "1573b70b7feb6458bb9955134d8aa0b3435c243c",
            "Origin": "https://www.builtinla.com",
            "DNT": "1",
            "Connection": "keep-alive",
            'Referer': "https://www.builtinla.com/",
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "cross-site",
            "Sec-GPC": "1",
            "Pragma": "no-cache",
            "Cache-Control": "no-cache",
            "TE": "trailers"
        }
        self._search_base_params = {
            "categories": "",
            "subcategories": "",
            "experiences": "",
            "industry": "",
            "regions": "",
            "locations": unquote("9%2C41%2C10%2C12%2C11%2C13%2C14%2C15%2C50%2C16%2C17"),
            "remote": "2",
            "per_page": "10",
            "page": "1",
            "search": "",
            "sortStrategy": "recency",
            "job_locations": unquote(
                "3%7C9%2C3%7C41%2C3%7C10%2C3%7C12%2C3%7C11%2C3%7C13%2C3%7C14%2C3%7C15%2C3%7C50%2C3%7C16%2C3%7C17%2C3%7C0"),
            "company_locations": unquote(
                "3%7C9%2C3%7C41%2C3%7C10%2C3%7C12%2C3%7C11%2C3%7C13%2C3%7C14%2C3%7C15%2C3%7C50%2C3%7C16%2C3%7C17%2C3%7C0"),
            "jobs_board": "true",
            "national": "false"
        }

    @override
    def run_api(self, task_update_state):
        self._task_update_state = task_update_state
        params = self._search_base_params
        params.update({"search": self._what, "categories": str(self._job_category)})
        jobs_search_request = RequestFields(
            path=self._search_path,
            params=params,
            headers=self._search_headers
        )
        res = self.make_request_for_fields(jobs_search_request)
        data = res.json()
        page_count = int(data.get("pagination_count", 1))
        self._page_count_with_limit = min(page_count, self._limit)
        logging.info(f"page_count {page_count}")
        self.process_request_for_search(res)
        count_deleted = BaseSearch.remove_job_duplicates()
        self._task_state_meta['job_duplicates_current'] += count_deleted
        self._task_state_meta['total'] = self._page_count_with_limit
        self._task_state_meta['current'] += 1
        self._task_state_meta['job_count'] = data.get("job_count", 0)
        self.update_state()
        if self._limit > 1:
            for p in range(2, self._page_count_with_limit + 1):
                logging.info(f"Page {p}")
                jobs_search_request.params.update({"page": str(p)})
                res = self.make_request_for_fields(jobs_search_request)
                self.process_request_for_search(res)
                self._task_state_meta['current'] += 1
                self.update_state()
        logging.info("Done")

    @staticmethod
    def make_request_for_fields(request_fields: RequestFields):
        time.sleep(3)
        return requests.get(request_fields.url,
                            params=request_fields.params,
                            headers=request_fields.headers)

    def more_company_details(self, company: dict):
        alias: str = company.get("alias").replace("/company/", "")
        region_id: int = company.get("region_id")
        company_req = RequestFields(
            path=f"{self._company_base_path}{alias}",
            params={"region_id": str(region_id)},
            headers=self._company_headers
        )
        res = self.make_request_for_fields(company_req)
        return res.json()

    def process_request_for_search(self, res: requests.Response):
        company_jobs = res.json().get("company_jobs")
        for cj in company_jobs:
            beacon_company = BuiltinBeacon()
            company:dict = cj.get("company")
            company_in_db = Company.query.filter_by(profile_url=f"https://builtin.com{company.get('alias')}").first()
            if not company_in_db:
                company.update(self.more_company_details(company))
                beacon_company.parse_company(company)
                company_in_db = self.insert_or_update_company_db(beacon_company)
            jobs = cj.get("jobs")
            for j in jobs:
                beacon = BuiltinBeacon()
                beacon.populate_company_from_bec(beacon_company)
                beacon.parse_job(j)
                job_in_db = self.insert_or_update_job_db(beacon)
                job_in_db.company_id = company_in_db.id
                search_in_db = Search(
                    job_board_name="Builtin",
                    job_id=job_in_db.id,
                    search_model_id=self._search_model_id,
                    task_id=self._task_id
                )
                db.session.add(search_in_db)
                db.session.commit()



