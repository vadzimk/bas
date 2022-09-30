""" checks if model_ids are valid for the user and executes update"""
import json
from typing import List

import pandas as pd

from bas_app import db
from bas_app.models import SearchModel, Search


def update_search_models(user_id: int, model_ids: List[int], values: dict):
    stmt = db.session.query(SearchModel.id) \
        .join(SearchModel.searches) \
        .filter(Search.user_id == user_id) \
        .filter(SearchModel.id.in_(model_ids)).distinct()
    search_models_in_db = stmt.all()
    if not search_models_in_db:
        return False
    else:
        db.session.query(SearchModel)\
            .filter(SearchModel.id.in_(model_ids)).update(values)
        db.session.commit()
        return True


def get_cards_for_user(user_id: int):
    stmt = db.select(SearchModel, Search.job_board_name) \
        .join(SearchModel.searches) \
        .filter(Search.user_id == user_id)\
        .filter(SearchModel.is_deleted == False)\
        .distinct()
    df = pd.read_sql(stmt, db.session.bind)
    table_json = json.loads(df.to_json(orient='records'))
    return table_json