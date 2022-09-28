import json
from typing import Type, List

import pandas as pd
from sqlalchemy import LABEL_STYLE_TABLENAME_PLUS_COL, or_

from bas_app import db
from bas_app.models import Job, Company, Search, CompanyUserNote
from .columns_to_display import columns


def get_current_data():
    result = db.session.query(Job, Company) \
        .join(Job) \
        .filter(Job.is_deleted == False) \
        .set_label_style(LABEL_STYLE_TABLENAME_PLUS_COL).statement

    df = pd.read_sql(result, db.session.bind)
    # print(df.info())

    df = df.reindex(columns=columns)

    # logging.info(f'info: {df.info()}')

    table_json = json.loads(df.to_json(orient='records'))
    return table_json


def get_jobs_with_flags(flag: bool, user_id: int):
    stmt = db.select(Job, Company) \
        .join(Search.jobs) \
        .filter(Job.is_deleted == False) \
        .filter(flag == True) \
        .filter(Search.user_id == user_id) \
        .join(Job.company) \
        .set_label_style(LABEL_STYLE_TABLENAME_PLUS_COL).distinct()
    df = pd.read_sql(stmt, db.session.bind)
    df = df.reindex(columns=columns)
    # logging.info(f'info: {df.info()}')
    table_json = json.loads(df.to_json(orient='records'))
    return table_json


def get_did_apply(user_id: int):
    return get_jobs_with_flags(Job.did_apply_flag, user_id)


def get_plan_apply(user_id: int):
    return get_jobs_with_flags(Job.plan_apply_flag, user_id)


def get_current_data_for_models(models: List[int], user_id: int):
    result = db.select(Job, Company, CompanyUserNote.note) \
        .join(Search.jobs) \
        .filter(Job.is_deleted == False) \
        .filter(Job.plan_apply_flag == False) \
        .filter(Job.did_apply_flag == False) \
        .filter(Search.search_model_id.in_(models)) \
        .filter(Search.user_id == user_id) \
        .join(Job.company) \
        .outerjoin(CompanyUserNote) \
        .filter(or_(CompanyUserNote.is_filtered == None, CompanyUserNote.is_filtered == False)) \
        .set_label_style(LABEL_STYLE_TABLENAME_PLUS_COL).distinct()
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
    return record


def update_one(record, user_id: int = None):
    """
    updates one record but does not call db.session.commit() yet
    :returns True if success False is failed
    """
    job_id = record.pop('job_id', None)  # records are prefixed with table_name_
    record_for_job_update = make_record_for_update(record, Job)
    record_for_company_update = make_record_for_update(record, Company)
    record_for_company_user_note_update = make_record_for_update(record, CompanyUserNote)
    touched = 0
    job = Job.query.get(job_id)
    if record_for_job_update:  # empty dict evaluate to false
        touched += db.session.query(Job).filter(Job.id == job_id).update(record_for_job_update)
    if record_for_company_update:
        touched += db.session.query(Company).filter(Company.id == job.company_id).update(record_for_company_update)
    if record_for_company_user_note_update:  # empty dict evaluate to false
        touched += db.session.query(CompanyUserNote).filter(CompanyUserNote.company_id == job.company_id, CompanyUserNote.user_id ==user_id).update(record_for_company_user_note_update)
    if not touched:
        return False
    db.session.commit()
    return True


def delete_many_jobs(records):
    db.session.query(Job) \
        .filter(Job.id.in_(tuple(records))) \
        .update({Job.is_deleted: True})
    db.session.commit()


def update_company_user_note(company_id: int, user_id: int, fields: dict):
    existing_company_user_note = CompanyUserNote.query.filter_by(user_id=user_id, company_id=company_id).first()
    if existing_company_user_note:
        for k, v in fields.items():
            setattr(existing_company_user_note, k, v)
    else:
        new_company_user_note = CompanyUserNote(
            user_id=user_id,
            company_id=company_id,
            **fields
        )
        db.session.add(new_company_user_note)
    db.session.commit()
