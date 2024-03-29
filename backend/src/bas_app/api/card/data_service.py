""" checks if model_ids are valid for the user and executes update"""
import json
from typing import List

import pandas as pd
from sqlalchemy import func

from bas_app import db
from bas_app.models import SearchModel, Search


def update_search_models(user_id: int, model_ids: List[int], values: dict):
    stmt = db.session.query(SearchModel.id) \
        .outerjoin(SearchModel.searches) \
        .filter(SearchModel.user_id == user_id) \
        .filter(SearchModel.id.in_(model_ids)).distinct()
    search_models_in_db = stmt.all()
    print(stmt)
    if not search_models_in_db:
        return False
    else:
        db.session.query(SearchModel)\
            .filter(SearchModel.id.in_(model_ids)).update(values)
        db.session.commit()
        return True


def get_cards_for_user(user_id: int):
    subq = db.select(SearchModel, Search.job_board_name, Search.task_id) \
        .join(SearchModel.searches) \
        .filter(SearchModel.user_id == user_id) \
        .filter(SearchModel.is_deleted == False) \
        .distinct().subquery()
    stmt = db.select(func.max(subq.c.id).label("id"), subq.c.what, subq.c.where, subq.c.age, subq.c.radius,
                     subq.c.experience, subq.c.job_category, subq.c.job_board_name, subq.c.task_id) \
        .group_by(subq.c.what, subq.c.where, subq.c.age, subq.c.radius, subq.c.experience, subq.c.job_category, subq.c.job_board_name, subq.c.task_id)
    df = pd.read_sql(stmt, db.session.bind)
    table_json = json.loads(df.to_json(orient='records'))
    return table_json