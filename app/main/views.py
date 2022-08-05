import json

import pandas as pd
from flask import render_template

from . import main
from .. import db
from ..models import Company, Job


@main.route('/', methods=['GET', 'POST'])
@main.route('/index', methods=['GET', 'POST'])
def index():
    result = db.session.query(Company, Job).join(Company).all()
    job_list = []
    for c, j in result:
        j_dict = j.__dict__
        j_dict.pop('_sa_instance_state', None)
        c_dict = c.__dict__
        c_dict.pop('_sa_instance_state', None)
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
    print(df.index)
    print(df)

    table_json = json.loads(df.to_json(orient='records'))
    # TODO add button start scrape , can be done using Celery
    # TODO add functionality on delete row marked deleted in db
    return render_template("index.html",
                           title="BAS",
                           table_json=table_json,
                           fields=df.columns.values)
