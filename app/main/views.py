import json

import pandas as pd
from flask import render_template, request, jsonify, redirect

from . import main
from .. import db
from ..models import Company, Job


@main.route('/', methods=['GET', 'POST'])
@main.route('/index', methods=['GET', 'POST'])
def index():
    # TODO add button start scrape , can be done using Celery
    # TODO add functionality on delete row marked deleted in db
    return render_template("index.html", title="BAS")


@main.route('/jobs', methods=['GET'])
def jobs():
    return jsonify(get_current_data())


@main.route('/job', methods=['DELETE'])
def job():
    records = json.loads(request.data)
    db.session.query(Job)\
        .filter(Job.id.in_(tuple(records)))\
        .update({Job.is_deleted: True})
    db.session.commit()
    return jsonify(get_current_data())


def get_current_data():
    result = db.session.query(Company, Job) \
        .join(Company) \
        .filter(Job.is_deleted == False) \
        .all()
    job_list = []

    for c, j in result:
        j_dict = j.__dict__
        j_dict.pop('_sa_instance_state', None)
        c_dict = c.__dict__
        c_dict.pop('_sa_instance_state', None)
        c_dict.pop('id', None)
        job_list.append({**j_dict, **c_dict})
    df = pd.json_normalize(job_list, sep='_')
    df.fillna('', inplace=True)
    # prepare the view
    df.sort_values(['rating', 'name', 'title'], ascending=[False, True, True], inplace=True)
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
        'profile_url',
        'homepage_url',
        'url',
    ]
    df = df.reindex(columns=columns)

    print('info', df.info())

    table_json = json.loads(df.to_json(orient='records'))
    return table_json
