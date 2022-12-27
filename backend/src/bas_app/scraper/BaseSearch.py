from abc import ABC, abstractmethod
from typing import Type

from bas_app import db
from bas_app.models import Job, Company
from bas_app.scraper.BaseBeacon import BaseBeacon


class BaseSearch(ABC):
    def __init__(self, *, user_id, search_model_id, task_id):
        self._task_update_state = None
        self._task_state_meta = {
            'total': 0,  # page_count + beacon count
            'current': 0,
            'job_count': 0,
            'job_duplicates_current': 0
        }
        self._page_count_with_limit = None
        self._total_skipped = 0,
        self._user_id = user_id,
        self._search_model_id = search_model_id,
        self._task_id = task_id

    @property
    def meta(self):
        return self._task_state_meta

    def update_state(self):
        self._task_update_state(state='PROGRESS', meta=self._task_state_meta)

    @staticmethod
    def insert_or_update_job_db(beacon: BaseBeacon):
        """ creates or updates job record in db"""
        return BaseSearch.insert_or_update_relation_helper(
            Table=Job,
            fields=beacon.job_attributes_only,
            filter_column='url',
            filter_value=beacon.dict.get('url')
        )

    @staticmethod
    def insert_or_update_relation_helper(Table: db.Model, fields: dict, filter_column: str, filter_value: str):
        """ generic insert or update relation into db
        inserts a new row or updates it if exists
        :Table: db.Model to insert fields
        :fields: fields of the row {attribute:value}
        :filter_column: where column
        :filter_value: where value
        :return: query row result
        """
        where = {filter_column: filter_value}
        existing_row = Table.query.filter_by(**where).first()
        if not existing_row:  # create record
            new_row = Table(**fields)
            db.session.add(new_row)
        else:  # update record
            for k, v in fields.items():
                if v:
                    setattr(existing_row, k, v)
        db.session.commit()
        return existing_row or new_row

    @staticmethod
    def insert_or_update_company_db(beacon: BaseBeacon):
        """ saves company fields of the beacon to db if company not present in db"""
        company = BaseSearch.insert_or_update_relation_helper(
            Table=Company,
            fields=beacon.dict['company'],
            filter_column='profile_url',
            filter_value=beacon.dict['company'].get('profile_url')
        )
        return company

    @abstractmethod
    def run_api(self, task_update_state):
        """
        :param task_update_state: update func from celery
        execute api search and save results in database
        """
        pass