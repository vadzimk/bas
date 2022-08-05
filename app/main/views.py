import json

import pandas as pd
from flask import render_template

from . import main


@main.route('/', methods=['GET', 'POST'])
@main.route('/index', methods=['GET', 'POST'])
def index():
    df: pd.DataFrame = pd.read_pickle('app/scraper/dataframe.pickle')


    print(df.index)
    print(df)

    table_json = json.loads(df.to_json(orient='records'))
    # TODO on post render button start scrape , can be done using Celery
    return render_template("index.html",
                           title="BAS",
                           table_json=table_json,
                           fields=df.columns.values)
