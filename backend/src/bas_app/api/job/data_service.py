import json
from typing import Type, List

import pandas as pd
from sqlalchemy import LABEL_STYLE_TABLENAME_PLUS_COL, or_

from bas_app import db
from bas_app.models import Job, Company, Search, CompanyUserNote, JobUserNote, SearchModel
from .columns_to_display import columns


def get_current_data(user_id):
    """ with all models """
    stmt = db.select(Job,
                     Company,
                     CompanyUserNote.note,
                     JobUserNote.note,
                     JobUserNote.plan_apply_flag,
                     JobUserNote.did_apply_flag) \
        .join(Search.jobs) \
        .join(Job.company) \
        .outerjoin(Job.noted_by_user) \
        .outerjoin(Company.noted_by_user) \
        .filter(or_(JobUserNote.is_filtered == False, JobUserNote.is_filtered == None)) \
        .filter(or_(JobUserNote.plan_apply_flag == False, JobUserNote.plan_apply_flag == None)) \
        .filter(or_(JobUserNote.did_apply_flag == False, JobUserNote.did_apply_flag == None)) \
        .filter(JobUserNote.user_id == user_id) \
        .filter(or_(CompanyUserNote.is_filtered == None, CompanyUserNote.is_filtered == False)) \
        .set_label_style(LABEL_STYLE_TABLENAME_PLUS_COL).distinct()
    df = pd.read_sql(stmt, db.session.bind)
    df = df.reindex(columns=columns)
    # logging.info(f'info: {df.info()}')
    table_json = json.loads(df.to_json(orient='records'))
    return table_json


def get_jobs_with_flags(flag: bool, user_id: int):
    """
    :flag: one of [JobUserNote.plan_apply_flag, JobUserNote.did_apply_flag]
    :return: jobs with true flag and not deleted"""
    stmt = db.select(Job,
                     Company,
                     CompanyUserNote.note,
                     JobUserNote.note,
                     JobUserNote.plan_apply_flag,
                     JobUserNote.did_apply_flag) \
        .join(Search.jobs) \
        .filter(JobUserNote.is_filtered == False) \
        .filter(flag == True) \
        .filter(JobUserNote.user_id == user_id) \
        .join(Job.company) \
        .outerjoin(CompanyUserNote) \
        .outerjoin(JobUserNote) \
        .set_label_style(LABEL_STYLE_TABLENAME_PLUS_COL).distinct()
    df = pd.read_sql(stmt, db.session.bind)
    df = df.reindex(columns=columns)
    # logging.info(f'info: {df.info()}')
    table_json = json.loads(df.to_json(orient='records'))
    return table_json


def get_did_apply(user_id: int):
    return get_jobs_with_flags(JobUserNote.did_apply_flag, user_id)


def get_plan_apply(user_id: int):
    return get_jobs_with_flags(JobUserNote.plan_apply_flag, user_id)


def get_current_data_for_models(models: List[int], user_id: int):
    stmt = db.select(Job,
                     Company,
                     CompanyUserNote.note,
                     JobUserNote.note,
                     JobUserNote.plan_apply_flag,
                     JobUserNote.did_apply_flag) \
        .join(Search.jobs) \
        .join(SearchModel, SearchModel.id == Search.search_model_id) \
        .filter(or_(JobUserNote.is_filtered == False, JobUserNote.is_filtered == None)) \
        .filter(or_(JobUserNote.plan_apply_flag == False, JobUserNote.plan_apply_flag == None)) \
        .filter(or_(JobUserNote.did_apply_flag == False, JobUserNote.did_apply_flag == None)) \
        .filter(Search.search_model_id.in_(models)) \
        .filter(SearchModel.user_id == user_id) \
        .join(Job.company) \
        .outerjoin(CompanyUserNote) \
        .filter(or_(CompanyUserNote.is_filtered == None, CompanyUserNote.is_filtered == False)) \
        .outerjoin(JobUserNote) \
        .set_label_style(LABEL_STYLE_TABLENAME_PLUS_COL).distinct()
    df = pd.read_sql(stmt, db.session.bind)
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
    record = {k: v for k, v in record.items() if
              k.startswith((table_name + "_"))}  # filters only  columns for this model
    print(f'only columns for {table_name}', record)
    record = {k.removeprefix((table_name + "_")): v for k, v in record.items()}  # removes the prefix table name
    return record


def update_one(record, user_id: int = None):
    """
    updates one record
    :returns True if success False is failed
    """
    job_id = record.pop('job_id', None)  # records are prefixed with table_name_
    record_for_job_update = make_record_for_update(record, Job)
    record_for_company_update = make_record_for_update(record, Company)
    record_for_company_user_note_update = make_record_for_update(record, CompanyUserNote)
    record_for_job_user_note_update = make_record_for_update(record, JobUserNote)
    print('record_for_job_user_note_update', record_for_job_user_note_update)
    touched = 0
    job = Job.query.get(job_id)
    if record_for_job_update:  # empty dict evaluate to false
        touched += db.session.query(Job).filter(Job.id == job_id).update(record_for_job_update)
    if record_for_company_update:
        touched += db.session.query(Company).filter(Company.id == job.company_id).update(record_for_company_update)
    if record_for_company_user_note_update:
        existing_company_user_note_query = db.session.query(CompanyUserNote) \
            .filter(CompanyUserNote.company_id == job.company_id,
                    CompanyUserNote.user_id == user_id)
        existing_company_user_note = existing_company_user_note_query.first()
        if existing_company_user_note:
            touched += existing_company_user_note_query.update(record_for_company_user_note_update)
        else:
            new_company_user_note = CompanyUserNote(
                user_id=user_id,
                company_id=job.company_id,
                **record_for_company_user_note_update
            )
            db.session.add(new_company_user_note)
            touched += 1
    if record_for_job_user_note_update:
        existing_job_user_note_query = db.session.query(JobUserNote) \
            .filter(JobUserNote.job_id == job.id,
                    JobUserNote.user_id == user_id)
        existing_job_user_note = existing_job_user_note_query.first()
        if existing_job_user_note:
            touched += existing_job_user_note_query.update(record_for_job_user_note_update)
        else:
            new_job_user_note = JobUserNote(
                job_id=job_id,
                user_id=user_id,
                **record_for_job_user_note_update)
            db.session.add(new_job_user_note)
            touched += 1
    db.session.commit()
    if not touched:
        return False
    return True


def delete_many_jobs(job_ids, user_id):
    records = [{"job_id": job_id, "JobUserNote_is_filtered": True} for job_id in job_ids]
    for record in records:
        update_one(record, user_id)


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
