from bs4 import BeautifulSoup

from BaseBrowserBeacon import BaseBrowserBeacon
from typing import List, Optional
from pandas import pandas as pd
from pandas import DataFrame

from abc import ABC, abstractmethod

from bas_app import db
from bas_app.models import Job, Search


class BasePage(ABC):
    JOBS_ON_PAGE = None

    def __init__(self, page_index: int, url: str):
        self._page_index = page_index
        self._soup: Optional[BeautifulSoup] = None
        self._job_count: Optional[int] = None
        self._beacons: Optional[List[BaseBrowserBeacon]] = None

    @property
    def job_count(self) -> int:
        return self._job_count

    @property
    def beacons(self) -> List[BaseBrowserBeacon]:
        return self._beacons

    @abstractmethod
    def count_total_jobs(self, ) -> int:
        """
        :return: number of jobs that the Indeed query returns
        """
        pass

    @abstractmethod
    def make_beacon_list(self) -> List[BaseBrowserBeacon]:
        pass

    def save_beacons_csv(self):
        df: DataFrame = pd.DataFrame(beacon.dict for beacon in self._beacons)
        df.to_csv(f'out/page{self._page_index}.csv')

    @abstractmethod
    async def populate(self, bpage):
        """ makes beacon list and saves to self._beacons """
        pass

    def save_beacons_job_db(self, user_id, search_model_id, task_id,):
        """ saves self._beacons job fields to Job and Search tables after the beacons on the search page have
        been scrolled
        """
        # TODO jobs are now saved only after beacons are collected. need to save them on beacon creation. to reduce memory usage
        for b in self._beacons:
            job = Job.query.filter_by(url=b.dict.get('url')).first()

            if not job:
                job = Job(**b.job_attributes_only)
                db.session.add(job)
                db.session.commit()

            match self.__class__.__name__:
                case "LinkedinPage":
                    job_board_name = 'Linkedin'
                case "IndeedPage":
                    job_board_name = 'Indeed'
                case _:
                    raise Exception('did not match classname in BasePage.save_beacons_job_db')

            search_in_db = Search(
                job_board_name=job_board_name,
                job_id=job.id,
                search_model_id=search_model_id,
                task_id=task_id
            )
            db.session.add(search_in_db)
            db.session.commit()
