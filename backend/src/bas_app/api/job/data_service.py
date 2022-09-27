import json
from typing import Type, List

import pandas as pd
from sqlalchemy import LABEL_STYLE_TABLENAME_PLUS_COL

from bas_app import db
from bas_app.models import Job, Company, Search
from .columns_to_display import columns


def get_current_data():
    result = db.session.query(Job, Company) \
        .join(Job) \
        .filter(Job.is_deleted == False)\
        .set_label_style(LABEL_STYLE_TABLENAME_PLUS_COL).statement

    df = pd.read_sql(result, db.session.bind)
    # print(df.info())

    df = df.reindex(columns=columns)

    # logging.info(f'info: {df.info()}')

    table_json = json.loads(df.to_json(orient='records'))
    return table_json


def get_current_data_for_models(models: List[int], user_id: int):
    # return get_current_data()
    # TODO revert this
    result = db.session.query(Job, Company) \
        .join(Search.jobs) \
        .filter(Job.is_deleted == False)\
        .filter(Search.search_model_id.in_(models)) \
        .filter(Search.user_id == user_id) \
        .join(Job.company)\
        .set_label_style(LABEL_STYLE_TABLENAME_PLUS_COL).distinct().statement

    df = pd.read_sql(result, db.session.bind)

    df = df.reindex(columns=columns)

    # logging.info(f'info: {df.info()}')

    table_json = json.loads(df.to_json(orient='records'))
    return table_json


def make_record_for_update(record: dict, model: Type[db.Model]):
    """
    :returns: dict that contains column:new_value for the table model
    :record: record to update
    :model: model of the table to get the column names from
    """
    table_name = model.__table__.name
    print('table_name', table_name)
    record = {k: v for k, v in record.items() if
              k.startswith((table_name + "_"))}  # filters only  columns for this model
    print('only columns for this model', record)
    record = {k.removeprefix((table_name + "_")): v for k, v in record.items()}  # removes the prefix table name
    print('removes the prefix table name', record)
    print('record_out', record)
    return record


def update_one(record):
    """
    updates one record but does not call db.session.commit() yet
    :returns True if success False is failed
    """
    id = record.pop('job_id', None)  # records are prefixed with table_name_
    record_for_job_update = make_record_for_update(record, Job)
    print('record_for_job_update', record_for_job_update)
    record_for_company_update = make_record_for_update(record, Company)
    print('record_for_company_update', record_for_company_update)
    touched = 0
    if record_for_job_update:  # empty dict evaluate to false
        touched += db.session.query(Job).filter(Job.id == id).update(record_for_job_update)
    if record_for_company_update:
        job = Job.query.get(id)
        touched += db.session.query(Company).filter(Company.id == job.company_id).update(record_for_company_update)
    if not touched:
        return False
    return True
