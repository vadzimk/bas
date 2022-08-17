import json
import logging

import pandas as pd
from flask import render_template, request, jsonify, Response


from . import main

from .. import db
from ..models import Company, Job
from ..main.tasks import scrape_linkedin


@main.route('/', )
@main.route('/index')
def index():
    # TODO add button start scrape , can be done using Celery
    # TODO add functionality on delete row marked deleted in db
    return render_template("index.html", title="BAS")


@main.route('/results')
def results():
    return render_template("results.html", title="BAS")


@main.route('/api/jobs', methods=['GET'])
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
    form_values = json.loads(request.data)
    print("form_values", form_values)
    # TODO add field search_type

    scrape_linkedin(form_values)
    return Response(status=202)


def get_current_data():
    # result = db.session.query(Company, Job) \
    #     .join(Company) \
    #     .filter(Job.is_deleted == False).statement
    result = db.session.query(Job, Company) \
        .join(Job) \
        .filter(Job.is_deleted == False).statement

        # .all()
    # job_list = []
    #
    # for c, j in result:
    #     j_dict = j.__dict__
    #     j_dict.pop('_sa_instance_state', None)
    #     c_dict = c.__dict__
    #     c_dict.pop('_sa_instance_state', None)
    #     c_dict.pop('id', None)
    #     job_list.append({**j_dict, **c_dict})
    # df = pd.json_normalize(job_list, sep='_')
    # df.fillna('', inplace=True)

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

