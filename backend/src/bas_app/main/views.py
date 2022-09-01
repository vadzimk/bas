import json

from typing import Type

import pandas as pd
from flask import render_template, request, jsonify, Response, send_from_directory
from sqlalchemy import inspect, LABEL_STYLE_TABLENAME_PLUS_COL

from . import main

from .. import db
from ..models import Company, Job, User, SearchModel
from ..main.tasks import scrape_linkedin


@main.route('/', )
@main.route('/index')
def index():
    # TODO add button start scrape , can be done using Celery
    # TODO add functionality on delete row marked deleted in db
    # return render_template("index.html", title="BAS")
    return send_from_directory('static', 'index.html')  # TODO temporarily serves react build from static folder


@main.route('/results')
def results():
    return render_template("results.html", title="BAS")


@main.route('/api/jobs')
def jobs():
    return jsonify(get_current_data())


@main.route('/api/job', methods=['DELETE'])
def delete_job():
    records = json.loads(request.data)
    print(records)
    db.session.query(Job) \
        .filter(Job.id.in_(tuple(records))) \
        .update({Job.is_deleted: True})
    db.session.commit()
    return jsonify(get_current_data())


def make_record_for_update(record: dict, model: Type[db.Model]):
    """
    :returns dict that contains column:new_value for the table model
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


@main.route('/api/job', methods=['PUT'])
def update_job():
    record = json.loads(request.data)
    print('record:', record)
    success = update_one(record)
    db.session.commit()
    if not success:
        return Response(status=400)
    return jsonify(get_current_data())


@main.route('/api/jobs', methods=['PUT'])
def update_many_jobs():
    """ currently only undo delete jobs """
    records = json.loads(request.data)
    print('records:', records)
    for rec in records:
        success = update_one(rec)
        if not success:
            return Response(status=400)
    db.session.commit()
    return jsonify(get_current_data())


@main.route('/api/search', methods=['POST'])
def search():
    data: dict = json.loads(request.data)
    print("data", data)
    user_id = data.pop('user_id', None)
    print("form_values", data)
    print('userid', user_id)
    # TODO add field search_type
    user = User.query.get_or_404(user_id)
    linkedin_credentials = {'email': user.linkedin_email, 'password': user.linkedin_password}
    print('linkedin_credentials', linkedin_credentials)
    search_model = SearchModel(
        what=data.get('what'),
        where=data.get('where'),
        age=data.get('age'),
        radius=data.get('radius'),
        experience=data.get('experience')
    )
    db.session.add(search_model)
    db.session.commit()
    task = scrape_linkedin.s(search_fields=data, linkedin_credentials=linkedin_credentials).apply_async()
    print("task.id", task.id)
    return jsonify({'task_id': task.id, 'model_id': search_model.id}), 202


@main.route('/api/status/<task_id>')
def search_status(task_id):
    """
    :param task_id:
    :return: {
    "state": "PROGRESS" | "BEGUN" | "REVOKED" | "SUCCESS"
    "info": {  # up to date version in BaseSearch.py
        "total": int,
        "current": int,
        "job_count": int
    }
}
    """
    task = scrape_linkedin.AsyncResult(task_id)
    if task.state == 'SUCCESS':
        info = task.get()
    elif task.state == 'PROGRESS':
        info = task.info
    else:
        info = str(task.info)
    response = {
        'state': task.state,
        'info': info
    }
    return jsonify(response)


@main.route('/api/revoke', methods=['POST'])
def search_revoke():
    task_id = request.get_json().get('task_id')
    scrape_linkedin.AsyncResult(task_id).revoke(terminate=True, signal='SIGKILL')

    return Response(status=204)


# TODO replace user management with flask login
@main.route('/api/user', methods=['PUT'])
def update_user():
    """
    user_details = {id, linkedin_email, linkedin_password}
    """
    user_details = request.get_json()
    print(user_details)
    user_id = user_details.get("id")
    print("user_id", user_id)
    user = User.query.get_or_404(user_id)
    # TODO add validation
    user.linkedin_email = user_details.get('linkedin_email')
    user.linkedin_password = user_details.get('linkedin_password')
    db.session.commit()
    linkedin_credentials = (user.linkedin_email and user.linkedin_password) and True
    return jsonify({"id": user.id, "linkedin_credentials": linkedin_credentials})


@main.route('/api/user', methods=['POST'])
def create_user():
    """
    user_details = {linkedin_email, linkedin_password, username}
    """
    user_details = request.get_json()
    print(user_details)
    username = user_details['username']
    user = User.query.filter_by(username=username).first()
    if user:
        return Response(f'username "{username}" already exists', status=409)
    user = User(
        username=username,
        linkedin_email=user_details.get('linkedin_email'),
        linkedin_password=user_details.get('linkedin_password')
    )
    db.session.add(user)
    db.session.commit()
    linkedin_credentials = (user.linkedin_email and user.linkedin_password) and True
    return jsonify({"id": user.id, "linkedin_credentials": linkedin_credentials})


@main.route('/api/user/login', methods=['POST'])
def login_user():
    """
    user_details = {username}
    """
    user_details = request.get_json()
    print("login", user_details)
    user = User.query.filter_by(username=user_details['username']).first()
    print('user:', user)
    if not user:
        return Response(status=404)
    linkedin_credentials = (user.linkedin_email and user.linkedin_password) and True
    return jsonify({"id": user.id, "linkedin_credentials": linkedin_credentials})


def get_current_data():
    result = db.session.query(Job, Company) \
        .join(Job) \
        .filter(Job.is_deleted == False).set_label_style(LABEL_STYLE_TABLENAME_PLUS_COL).statement

    df = pd.read_sql(result, db.session.bind)
    # print(df.info())

    columns = [
        'job_id',
        'job_title',
        'job_job_type',
        'job_qualifications',
        'job_salary',
        'job_estimated_salary',
        'job_date_posted',
        'job_multiple_candidates',
        'job_benefits',
        'job_description_markdown',
        'job_description_text',
        'job_description_html',
        'job_hiring_insights',
        'job_url',
        'company_name',
        'company_rating',
        'company_industry',
        'company_size',
        'company_overview',
        'company_number_employees',
        'company_location',
        'company_main_country_name',
        'company_main_country_number_employees',
        'company_other_locations_employees',
        'company_other_locations_employees_html',
        'company_profile_url',
        'company_homepage_url',
        'job_plan_apply_flag',
        'job_did_apply_flag',
        'job_note',
        'company_note',
    ]
    df = df.reindex(columns=columns)

    # logging.info(f'info: {df.info()}')

    table_json = json.loads(df.to_json(orient='records'))
    return table_json
