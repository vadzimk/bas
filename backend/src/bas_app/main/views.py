from flask import render_template, send_from_directory

from . import main


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

