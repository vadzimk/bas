import pandas as pd
from flask import jsonify, request

from . import card
from ... import db
from ...models import SearchModel, Search


@card.route('/api/cards')
def cards():
    user_id = int(request.args.get('user_id'))
    stmt = db.select(SearchModel, Search.job_board_name).join(SearchModel.searches).filter(Search.user_id == user_id).distinct()
    df = pd.read_sql(stmt, db.session.bind)
    return jsonify(df.to_json(orient='records'))
