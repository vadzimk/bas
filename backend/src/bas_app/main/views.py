import json
import logging

import pandas as pd
from flask import render_template, request, jsonify, Response, url_for, send_from_directory, send_file

from . import main

from .. import db
from ..models import Company, Job, User
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
    db.session.query(Job) \
        .filter(Job.id.in_(tuple(records))) \
        .update({Job.is_deleted: True})
    db.session.commit()
    return jsonify(get_current_data())


@main.route('/api/job', methods=['PUT'])
def update_job():
    record = json.loads(request.data)
    id = record['id']
    record.pop('id', None)
    print('record', record.keys())
    res = db.session.query(Job).filter(Job.id == id).update(record)
    db.session.commit()
    print("res", res)
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
    task = scrape_linkedin.s(search_fields=data, linkedin_credentials=linkedin_credentials).apply_async()
    print("task.id", task.id)
    return jsonify({'task_id': task.id}), 202


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
    return jsonify({'id': user.id})


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
        .filter(Job.is_deleted == False).statement

    df = pd.read_sql(result, db.session.bind)
    print(df.info())

    columns = [
        'id',
        'title',
        'job_type',
        'qualifications',
        'salary',
        'estimated_salary',
        'date_posted',
        'multiple_candidates',
        'benefits',
        'description_markdown',
        'description_text',
        'description_html',
        'hiring_insights',
        'name',
        'rating',
        'industry',
        'size',
        'overview',
        'number_employees',
        'location',
        'main_country_name',
        'main_country_number_employees',
        'other_locations_employees',
        'other_locations_employees_html',
        'plan_apply_flag',
        'did_apply_flag',
        'note',
        'profile_url',
        'homepage_url',
        'url',
    ]
    df = df.reindex(columns=columns)

    # logging.info(f'info: {df.info()}')

    table_json = json.loads(df.to_json(orient='records'))
    return table_json
